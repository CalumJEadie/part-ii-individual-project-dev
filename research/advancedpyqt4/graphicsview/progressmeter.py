#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a  
# progress meter using the
# GraphicsView framework
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: March 2010


from PyQt4 import QtGui, QtCore


class ProgressMeter(QtGui.QGraphicsItem):
    def __init__(self, parent):
        super(ProgressMeter, self).__init__()
        
        self.parent = parent
        
        self.angle = 0
        self.per = 0
        
    def boundingRect(self):
    
        return QtCore.QRectF(0, 0, self.parent.width(), 
                              self.parent.height())
        
    def increment(self):
    
        self.angle += 1
        self.per = int(self.angle / 3.6)
        if self.angle > 360:
            return False
        else:
            return True
        
    def paint(self, painter, option, widget):

        self.drawBackground(painter, widget)
        self.drawMeter(painter, widget)
        self.drawText(painter)
  
        
    def drawBackground(self, painter, widget):
    
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        
        p1 = QtCore.QPointF(80, 80)
        g = QtGui.QRadialGradient(p1*0.2, 80*1.1)

        g.setColorAt(0.0, widget.palette().light().color())
        g.setColorAt(1.0, widget.palette().dark().color())
        painter.setBrush(g)
        painter.drawEllipse(0, 0, 80, 80)
        
        p2 = QtCore.QPointF(40, 40)
        g = QtGui.QRadialGradient(p2, 70*1.3)

        g.setColorAt(0.0, widget.palette().midlight().color())
        g.setColorAt(1.0, widget.palette().dark().color())
        painter.setBrush(g)
        painter.drawEllipse(7.5, 7.5, 65, 65)
        
        
    def drawMeter(self, painter, widget):
    
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(widget.palette().highlight().color())
        painter.drawPie(7.5, 7.5, 65, 65, 0, -self.angle*16)
               
        
    def drawText(self, painter):
    
        text = "%d%%" % self.per
        
        font = painter.font()
        font.setPixelSize(11)
        painter.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor("#000000"))
        pen = QtGui.QPen(brush, 1)
        painter.setPen(pen)
        #size = painter.fontMetrics().size(QtCore.Qt.TextSingleLine, text)
        painter.drawText(0, 0, 80, 80, 
                          QtCore.Qt.AlignCenter, text)
    

class MyView(QtGui.QGraphicsView):
    def __init__(self):
        super(MyView, self).__init__()
        
        self.initView()
        self.setupScene()
        self.setupAnimation()
        
        self.setGeometry(300, 150, 250, 250)
        
    def initView(self):
    
        self.setWindowTitle("Progress meter")
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        policy = QtCore.Qt.ScrollBarAlwaysOff
        self.setVerticalScrollBarPolicy(policy)
        self.setHorizontalScrollBarPolicy(policy)
        
        self.setBackgroundBrush(self.palette().window())
        
        self.pm = ProgressMeter(self)
        self.pm.setPos(55, 55)
    

        
    def setupScene(self):
    
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 250, 250)
        self.scene.addItem(self.pm)
        
        self.setScene(self.scene)

        
    def setupAnimation(self):

        self.timer = QtCore.QTimeLine()
        self.timer.setLoopCount(0)
        self.timer.setFrameRange(0, 100)

        self.animation = QtGui.QGraphicsItemAnimation()
        self.animation.setItem(self.pm)
        self.animation.setTimeLine(self.timer)
        
        QtCore.QObject.connect(self.timer, 
            QtCore.SIGNAL("frameChanged(int)"), self.doStep)
        
        self.timer.start()
        
        
    def doStep(self, i):
        if not self.pm.increment():
            self.timer.stop()
        self.pm.update()
          
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    view = MyView()
    view.show()
    app.exec_()
