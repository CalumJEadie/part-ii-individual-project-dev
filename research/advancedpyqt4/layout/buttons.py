#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we put two buttons
# in the right bottom corner of the window
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui
              

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Buttons")
       
        self.initUI()
        
        
    def initUI(self):
    
        ok = QtGui.QPushButton("OK")
        cancel = QtGui.QPushButton("Cancel")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
                

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()


































