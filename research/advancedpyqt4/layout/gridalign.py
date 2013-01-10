#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we align widgets in
# QGridLayout manager
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: May 2010


from PyQt4 import QtGui, QtCore
      
        
class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle("Alignments")
       
        self.initUI()
        
        
    def initUI(self):
    
        button1 = QtGui.QPushButton("Left")
        button2 = QtGui.QPushButton("Center")
        button3 = QtGui.QPushButton("Right")
        button4 = QtGui.QPushButton("Stretch")


        grid = QtGui.QGridLayout()
        grid.addWidget(button1, 0, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(button2, 1, 0, QtCore.Qt.AlignCenter)
        grid.addWidget(button3, 2, 0, QtCore.Qt.AlignRight)
        grid.addWidget(button4, 3, 0)

        self.setLayout(grid)
                                

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
