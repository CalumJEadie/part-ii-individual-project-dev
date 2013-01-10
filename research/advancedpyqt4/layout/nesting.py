#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we demonstrate the nesting of 
# layout managers. 
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui      
        

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.move(300, 300)
        self.setWindowTitle("Nesting")
       
        self.initUI()
        
        
    def initUI(self):
    
        hbox = QtGui.QHBoxLayout()
        
        hbox.addStretch(1)
        hbox.addWidget(QtGui.QPushButton("Button")) 
        
        vbox1 = QtGui.QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addWidget(QtGui.QPushButton("Button"))
        vbox1.addWidget(QtGui.QPushButton("Button"))
        vbox1.addStretch(1)
        
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(QtGui.QPushButton("Button"))
        vbox2.addWidget(QtGui.QPushButton("Button"))
        vbox2.addWidget(QtGui.QPushButton("Button"))
        vbox2.addStretch(1)
               
        vbox3 = QtGui.QVBoxLayout()
        vbox3.addStretch(1)
        vbox3.addWidget(QtGui.QPushButton("Button"))
        vbox3.addWidget(QtGui.QPushButton("Button"))
        vbox3.addWidget(QtGui.QPushButton("Button"))
        vbox3.addWidget(QtGui.QPushButton("Button"))
        vbox3.addStretch(1)
        
        hbox.addLayout(vbox1)        
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)
        hbox.addStretch(1)
        
        self.setLayout(hbox) 
                

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
