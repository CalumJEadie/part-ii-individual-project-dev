#!/usr/bin/python
#
# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we demostrate
# how to span widgets in 
# QGridLayout manager
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: May 2010


from PyQt4 import QtCore, QtGui


class Example(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.move(300, 300)
        self.setWindowTitle("Spanning")
       
        self.initUI()


    def initUI(self):
                
        grid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLineEdit(), 0, 0)
        grid.addWidget(QtGui.QLineEdit(), 0, 1)
        grid.addWidget(QtGui.QLineEdit(), 0, 2)
        grid.addWidget(QtGui.QLineEdit(), 0, 3)
        
        grid.addWidget(QtGui.QLineEdit(), 1, 0, 1, 2)
        grid.addWidget(QtGui.QLineEdit(), 2, 0, 1, 3)
        grid.addWidget(QtGui.QLineEdit(), 3, 0, 1, 4)

        self.setLayout(grid)
       
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
