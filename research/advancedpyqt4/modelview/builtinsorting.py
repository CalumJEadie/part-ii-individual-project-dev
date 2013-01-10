#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we sort data in the
# QTableView widget
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: May 2010


from PyQt4 import QtGui, QtCore
   
FIRST_COLUMN = 0

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("Sorting")
       
        self.initData()
        self.initUI()

    def initData(self):
    
        names = QtCore.QStringList()
        names.append("Jack")
        names.append("Tom")
        names.append("Lucy")
        names.append("Bill")
        names.append("Jane")
        
        self.model = QtGui.QStringListModel(names)
           
            
    def initUI(self):
             
        self.tv = QtGui.QTableView(self)
        self.tv.setModel(self.model)
        self.tv.setSortingEnabled(True)

        sortB = QtGui.QPushButton("Sort", self)
        sortB.setSizePolicy(QtGui.QSizePolicy.Fixed, 
             QtGui.QSizePolicy.Fixed)
        
        self.sortType = QtGui.QCheckBox("Ascending", self)
        self.sortType.setSizePolicy(QtGui.QSizePolicy.Fixed, 
             QtGui.QSizePolicy.Fixed)
        
        self.connect(sortB, QtCore.SIGNAL('clicked()'), 
                      self.sortItems)
                      
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.sortType)
        hbox.addWidget(sortB)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tv) 
        vbox.addLayout(hbox)
        self.setLayout(vbox)  
        
    def sortItems(self):
        checked = self.sortType.isChecked()
        if checked:
            self.tv.sortByColumn(FIRST_COLUMN, 
                QtCore.Qt.AscendingOrder)
        else:
            self.tv.sortByColumn(FIRST_COLUMN, 
                QtCore.Qt.DescendingOrder)
            

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
