#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this examaple, we zoom 
# items on the QGraphicsView
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: March 2010


from PyQt4 import QtGui, QtCore
            

class View(QtGui.QGraphicsView):
    def __init__(self):
        super(View, self).__init__()
        
        self.setGeometry(300, 300, 300, 300)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
       
        self.init()
        
        
    def init(self):

        self.scene = QtGui.QGraphicsScene()
        
        r1 = self.scene.addRect(150, 40, 100, 100)
        r1.setBrush(QtGui.QColor(250, 50, 0))
        r1.setPen(QtGui.QColor(250, 50, 0))
               
        el = self.scene.addEllipse(40, 70, 80, 80)
        el.setBrush(QtGui.QColor(0, 50, 250))
        el.setPen(QtGui.QColor(0, 50, 250))
        
        r2 = self.scene.addRect(60, 180, 150, 70)
        r2.setBrush(QtGui.QColor(0, 250, 50))
        r2.setPen(QtGui.QColor(0, 250, 50))
        
        self.setScene(self.scene)  


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

        
    def initUI(self):
        
        vbox = QtGui.QVBoxLayout()

        self.view = View()
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setRange(1, 500)
        slider.setValue(100)
        self.connect(slider, 
            QtCore.SIGNAL('valueChanged(int)'), self.onZoom)
        
        vbox.addWidget(self.view)
        vbox.addWidget(slider)
        self.setLayout(vbox)
        self.setWindowTitle("Zoom")
        self.setGeometry(150, 150, 300, 300)
        
    
    def onZoom(self, value):
    
        val = value / 100.0      
        self.view.resetMatrix()
        self.view.scale(val, val)
    

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()


