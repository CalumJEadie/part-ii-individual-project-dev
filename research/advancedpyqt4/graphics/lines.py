#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we draw lines
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: August 2009


from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Lines')
        
        self.cs = [[0 for i in range(2)] for j in range(100)]
        self.count = 0

       
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawLines(painter)
        painter.end()
        
    def mousePressEvent(self, e):
        
        if e.button() == QtCore.Qt.LeftButton:

            x = e.x()
            y = e.y()

            self.cs[self.count][0] = x
            self.cs[self.count][1] = y
            self.count = self.count + 1
        
        if e.button() == QtCore.Qt.RightButton:
            self.repaint()
            self.count = 0
        

    def drawLines(self, painter):
    
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        painter.eraseRect(0, 0, w, h)

        for i in range(self.count):
            for j in range(self.count):
                painter.drawLine(self.cs[i][0], self.cs[i][1],  
                    self.cs[j][0], self.cs[j][1])


app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()