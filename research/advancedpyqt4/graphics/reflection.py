#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a reflected
# image
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010

import sys
from PyQt4 import QtGui, QtCore

GAP = 30
INITIAL_OPACITY = 0.7

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initExample()

        self.setGeometry(200, 200, 300, 400)
        self.setWindowTitle('Reflection')
        
    def initExample(self):
        
        self.img = QtGui.QImage("slanec.png")
        if self.img.isNull():
            print "Error loading image"
            sys.exit(1)
            
        self.iw = self.img.width()
        self.ih = self.img.height()
        
        self.opacity = 0.7
        self.step = self.opacity / self.ih

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawImage(painter)
        painter.end()
        
    def drawImage(self, painter):
    
        w = self.width()
        h = self.height()
        
        painter.fillRect(0, 0, w, h, QtCore.Qt.black)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = QtCore.QRect(25, 15, self.iw, self.ih)
        painter.drawImage(rect, self.img)
        painter.translate(0, 2*self.ih + GAP)
        painter.scale(1, -1)
        
        i = 0
        self.alpha = 0.7
        
        while i < self.ih:
            i = i + 1
            self.opacity = self.opacity - self.step
            painter.setOpacity(INITIAL_OPACITY - self.opacity)
            painter.drawImage(25, i, self.img, 0, i, -1, 1)
        
        
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
