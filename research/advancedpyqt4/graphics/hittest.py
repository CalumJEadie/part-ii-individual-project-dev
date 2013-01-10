#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we we work with a thread. 
# We click on the area of the rectangle and 
# the rectangle starts to fade away
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: August 2009


import time
from PyQt4 import QtGui, QtCore



class MyThread(QtCore.QThread):
    def __init__(self):
        super(MyThread, self).__init__()

        self.alpha = 1

    def run(self):
    
        print "Thread started"
        while self.alpha >= 0:
            self.alpha -= 0.01
            self.emit(QtCore.SIGNAL("fading(float)"), 
                self.alpha)             
            time.sleep(0.1)
        print "Thread ended"


class Example(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__()
        
        self.initExample()

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Hit test')
    
    def initExample(self):
    
        self.rect = QtCore.QRect(20, 20, 80, 80)
        self.alpha = 1
        self.m = MyThread()
        self.connect(self.m, QtCore.SIGNAL("fading(float)"), 
            self.fade, QtCore.Qt.QueuedConnection)
    
    def paintEvent(self, event):
    
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawRectangle(painter)
        painter.end()
        
    def fade(self, alpha):
    
        self.alpha = alpha
        #print self.alpha
        self.repaint()
        
    def mousePressEvent(self, e):
        
        if e.button() == QtCore.Qt.LeftButton \
            and self.alpha==1:

            x = e.x()
            y = e.y()
            
            if self.rect.contains(x, y):
               if not self.m.isRunning():   
                   self.m.start()
                
  
    def drawRectangle(self, painter):
    
        painter.setOpacity(self.alpha)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.black))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(self.rect)
    

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
