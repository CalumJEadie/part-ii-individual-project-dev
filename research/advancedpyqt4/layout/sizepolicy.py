#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we demonstrate the QSizePolicy
# layout attribute
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui
              

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.move(300, 300)
        self.setWindowTitle("Size policy")
       
        self.initUI()
        
        
    def initUI(self):
    
        btn1 = QtGui.QPushButton("Button", self)
        btn1.setSizePolicy(QtGui.QSizePolicy.Fixed, 
             QtGui.QSizePolicy.Fixed)
        btn2 = QtGui.QPushButton("Button", self)
        btn3 = QtGui.QPushButton("Button", self)
        btn3.setSizePolicy(QtGui.QSizePolicy.Fixed, 
             QtGui.QSizePolicy.Fixed)
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(btn1) 
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        self.setLayout(layout) 
                

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
