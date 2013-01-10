#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a Windows
# window with layout boxes
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
        hlpBtn.setSizePolicy(QtGui.QSizePolicy.Fixed, 
                              QtGui.QSizePolicy.Fixed)
        okBtn = QtGui.QPushButton("OK")
        
        listView = QtGui.QListView()
        
        vbox = QtGui.QVBoxLayout()
        hbox1 = QtGui.QHBoxLayout()
        
        hbox1.addWidget(windows)
        vbox.addLayout(hbox1)
        
        hbox2 = QtGui.QHBoxLayout()
        vboxl = QtGui.QVBoxLayout()
        vboxr = QtGui.QVBoxLayout()
        
        vboxl.addWidget(listView)
        vboxr.addWidget(actBtn)
        vboxr.addWidget(clsBtn)
       
        vboxr.setAlignment(clsBtn, QtCore.Qt.AlignTop)
        
        hbox2.addLayout(vboxl)
        hbox2.addLayout(vboxr)
        vbox.addLayout(hbox2)
        
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(hlpBtn)
        hbox3.addWidget(okBtn)
        hbox3.setAlignment(okBtn, QtCore.Qt.AlignRight)
        vbox.addLayout(hbox3)
        
        self.setLayout(vbox)
       
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
