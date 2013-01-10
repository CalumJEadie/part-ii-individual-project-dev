#!/usr/bin/python
#
# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we show three images
# using absolute positioning
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtGui


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 300, 280)
        self.setWindowTitle("Absolute")
       
        self.initUI()

    def initUI(self):
    
        self.setStyleSheet("background-color: #222222")
        
        bardejov = QtGui.QPixmap("bardejov.jpg")
        mincol = QtGui.QPixmap("mincol.jpg")
        rotunda = QtGui.QPixmap("rotunda.jpg")
        
        label1 = QtGui.QLabel(self)
        label2 = QtGui.QLabel(self)
        label3 = QtGui.QLabel(self)
        
        label1.setPixmap(bardejov)
        label2.setPixmap(mincol)
        label3.setPixmap(rotunda)
        
        label1.setGeometry(20, 20, 120, 90)
        label2.setGeometry(40, 160, 120, 90)
        label3.setGeometry(170, 50, 120, 90)
        
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
