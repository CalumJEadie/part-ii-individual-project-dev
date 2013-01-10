#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we demonstrate the maximum and
# minumim size
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui
              

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.move(300, 300)
        self.setWindowTitle("MinMax")
       
        self.initUI()
        
        
    def initUI(self):
    
        te = QtGui.QTextEdit()
        te.setMinimumSize(15, 15)
        te.setMaximumSize(350, 350)
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(te) 
        self.setLayout(layout) 
                

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
