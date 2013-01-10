#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# This is a basic QTableView example
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui
   

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("QTableView")
       
        self.initData()
        self.initUI()

    def initData(self):
    
        data = (2, 3, 6, 7, 3, 9, 12, 23)
        self.model = QtGui.QStandardItemModel(10, 6)
        
        row = 0
        col = 0
        
        for i in data:
            item = QtGui.QStandardItem(str((i)))
            self.model.setItem(row, col, item)
            row = row + 1
            
            
    def initUI(self):
             
        self.tv = QtGui.QTableView(self)
        self.tv.setModel(self.model)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tv) 
        self.setLayout(vbox)  
        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
