#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this examaple, we rotate a 
# rectangle
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: June 2010


from PyQt4 import QtGui, QtCore
      

class Rectangle(QtGui.QGraphicsRectItem):
    def __init__(self,x,y,w,h):
        super(Rectangle, self).__init__(x, y, w, h)
        
        self.setBrush(QtGui.QColor(250, 50, 0))
        self.setPen(QtGui.QColor(250, 50, 0))
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setCursor(QtCore.Qt.SizeAllCursor)
        
        self.tx = 200
        self.ty = 200
        
        
    def doRotate(self, alfa):
        
        tr = QtGui.QTransform()
        tr.translate(self.tx, self.ty)
        tr.rotate(alfa)
        tr.translate(-self.tx, -self.ty)
        
        self.setTransform(tr)
               
        

class View(QtGui.QGraphicsView):
    def __init__(self):
        super(View, self).__init__()
             
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.initScene()
        
        
    def initScene(self):
     

        self.scene = QtGui.QGraphicsScene()
        self.setSceneRect(0, 0, 400, 400)  
             
        self.rect = Rectangle(150, 150, 100, 100)        
        self.scene.addItem(self.rect)

        self.setScene(self.scene)  


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
       
        self.setWindowTitle("Rotation")
        self.setGeometry(150, 150, 300, 300)
       
        self.initUI()
       
       
    def initUI(self):   

        vbox = QtGui.QVBoxLayout()
        
        self.view = View()
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld.setRange(-180, 180)
        
        self.connect(sld, QtCore.SIGNAL('valueChanged(int)'), 
                      self.changeValue)
        
        vbox.addWidget(self.view)
        vbox.addWidget(sld)
        self.setLayout(vbox)
        
    
    def changeValue(self, value):

        self.view.rect.doRotate(value)     


app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
