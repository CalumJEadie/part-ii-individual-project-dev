#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we work with the
# stretch factor applied on empty space
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtGui
              

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 450, 200)
        self.setWindowTitle("Stretch space")
       
        self.initUI()
        
        
    def initUI(self):
    
        vbox = QtGui.QVBoxLayout()
               
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(QtGui.QPushButton("Button"))
        hbox1.addWidget(QtGui.QPushButton("Button"))
        
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(QtGui.QPushButton("Button"))
        hbox2.addWidget(QtGui.QPushButton("Button"))
        hbox2.addStretch(1)
               
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(QtGui.QPushButton("Button"))
        hbox3.addStretch(1)
        hbox3.addWidget(QtGui.QPushButton("Button"))
        
        hbox4 = QtGui.QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.addWidget(QtGui.QPushButton("Button"))
        hbox4.addWidget(QtGui.QPushButton("Button"))
        hbox4.addStretch(1)
        
        hbox5 = QtGui.QHBoxLayout()
        hbox5.addWidget(QtGui.QPushButton("Button"))
        hbox5.addStretch(1)
        hbox5.addWidget(QtGui.QPushButton("Button"))
        hbox5.addStretch(1)
                
        vbox.addLayout(hbox1)        
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
       
        self.setLayout(vbox) 
                

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
