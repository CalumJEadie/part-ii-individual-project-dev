#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# This is a very simple demonstration of
# the QGridLayout manager
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtGui


class Example(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.move(300, 300)
        self.setWindowTitle("Buttons")
       
        self.initUI()


    def initUI(self):
                
        button1 = QtGui.QPushButton("Button")
        button2 = QtGui.QPushButton("Button")
        button3 = QtGui.QPushButton("Button")
        button4 = QtGui.QPushButton("Button")
        button5 = QtGui.QPushButton("Button")
        button6 = QtGui.QPushButton("Button")

        grid = QtGui.QGridLayout()
        grid.addWidget(button1, 0, 0)
        grid.addWidget(button2, 0, 1)
        grid.addWidget(button3, 0, 2)
        grid.addWidget(button4, 1, 0)
        grid.addWidget(button5, 1, 1)
        grid.addWidget(button6, 1, 2)
        
        self.setLayout(grid)
       
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
