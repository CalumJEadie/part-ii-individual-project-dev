#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a Windows
# window with QGridLayout
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtCore, QtGui


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Windows")
       
        self.initUI()


    def initUI(self):
        
        windows = QtGui.QLabel('Windows')
        
        actBtn = QtGui.QPushButton("Activate")
        clsBtn = QtGui.QPushButton("Close")
        hlpBtn = QtGui.QPushButton("Help")
        okBtn = QtGui.QPushButton("OK")
        
        listView = QtGui.QListView()

        grid = QtGui.QGridLayout()

        grid.addWidget(windows, 0, 0)
        grid.addWidget(listView, 1, 0, 2, 2)

        grid.addWidget(actBtn, 1, 4)
        grid.addWidget(clsBtn, 2, 4)

        grid.addWidget(hlpBtn, 4, 0)
        grid.addWidget(okBtn, 4, 4)
        
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(2, 1)
        
        grid.setAlignment(clsBtn, QtCore.Qt.AlignTop)

        self.setLayout(grid)
       
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
