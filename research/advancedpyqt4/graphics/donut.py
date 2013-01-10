#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we draw a donut
# shape
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__()

        self.setGeometry(300, 300, 350, 280)
        self.setWindowTitle('Donut')

    def paintEvent(self, event):
    
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawDonut(painter)
        painter.end()
        
    def drawDonut(self, painter):

        brush = QtGui.QBrush(QtGui.QColor("#535353"))
        painter.setPen(QtGui.QPen(brush, 0.5))

        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        h = self.height()
        w = self.width()

        painter.translate(QtCore.QPoint(w/2, h/2))
         
        rot = 0
       
        while rot < 360.0:
            painter.drawEllipse(-125, -40, 250, 80)
            painter.rotate(5.0)
            rot += 5.0
        
   
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()