#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# This example demonstrates clipping
#
# author: jan bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Clipping')
        
        self.initExample()


    def initExample(self):
        
        self.rotate = 1
        self.pos_x = 8
        self.pos_y = 8
        self.radius = 60

        self.delta = [1, 1]
        self.timerId = self.startTimer(15)


    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawObjects(painter)
        painter.end()
        
    def drawObjects(self, painter):

        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        rect = QtCore.QRect(-100, -40, 200, 80)      

        painter.translate(w/2, h/2)
        painter.rotate(self.rotate)
        painter.drawRect(rect)
 
        brush = QtGui.QBrush(QtGui.QColor(110, 110, 110))
        painter.setBrush(brush)
        
        region = QtGui.QRegion(self.pos_x, self.pos_y, 
            self.radius, self.radius, QtGui.QRegion.Ellipse)
        painter.setClipRegion(region)
        painter.setClipRect(rect)

        painter.resetTransform()
        painter.drawEllipse(self.pos_x, self.pos_y, 
                self.radius, self.radius)
        
        painter.setBrush(QtCore.Qt.NoBrush)
        
        painter.setClipping(False)
        painter.drawEllipse(self.pos_x, self.pos_y, 
                self.radius, self.radius)
        
    def timerEvent(self, event):
        
        self.step()
        self.repaint()
        
        
    def step(self):
    
        w = self.width()
        h = self.height()
         
        if self.pos_x < 0:
            self.delta[0] = 1
        elif self.pos_x > w - self.radius:
            self.delta[0] = -1
       
        if self.pos_y < 0:
            self.delta[1] = 1
        elif self.pos_y > h - self.radius:
            self.delta[1] = -1
       
        self.pos_x += self.delta[0]
        self.pos_y += self.delta[1]
        
        self.rotate = self.rotate + 1

   
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()