#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we work with the sizeHint
# property
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtGui, QtCore
      

class MyButton(QtGui.QPushButton):
    def __init__(self, text, parent, size):
        super(MyButton, self).__init__(text, parent)
        
        self.size = size
        
    def sizeHint(self):
        return self.size


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 300, 230)
        self.setWindowTitle("Size hints")
       
        self.initUI()
        
        
    def initUI(self):
    
        button1 = QtGui.QPushButton("Button", self)
        button1.move(20, 50)
        
        button2 = MyButton("Button", self, 
                      QtCore.QSize(140, 27))
        button2.move(150, 50)
        
        button3 = MyButton("Button", self, 
                      QtCore.QSize(150, 60))
                      
        button3.move(50, 150)
      

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
