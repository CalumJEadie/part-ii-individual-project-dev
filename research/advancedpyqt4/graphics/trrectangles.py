#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we draw ten rectangles with
# different levels of opacity
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: August 2009


from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 590, 90)
        self.setWindowTitle('Transparent rectangles')

    def paintEvent(self, event):
    
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawRectangles(painter)
        painter.end()
        
    def drawRectangles(self, painter):
 
        for i in range(1, 11):
            painter.setOpacity(i*0.1)
            painter.fillRect(50*i, 20, 40, 40, 
                QtCore.Qt.darkGray)
    

app = QtGui.QApplication([])
example = Example()
example.show()
app.exec_()