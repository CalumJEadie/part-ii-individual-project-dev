#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we work with QModelIndex 
# and QTreeView
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui, QtCore
      
      
data = ( ["Jessica Alba", "Pomona", "1981"],   
       ["Angelina Jolie", "New York", "1975"],        
       ["Natalie Portman", "Yerusalem", "1981"],        
       ["Scarlett Jonahsson", "New York", "1984"] )
      
      

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("Actresses")
       
        self.initData()
        self.initUI()
    
    def initData(self):
    
        self.model = QtGui.QStandardItemModel()
        labels = QtCore.QStringList(("Name", "Place", "Born"))
        self.model.setHorizontalHeaderLabels(labels)
        
       
        for i in range(len(data)):
            name = QtGui.QStandardItem(data[i][0])
            place = QtGui.QStandardItem(data[i][1])
            born = QtGui.QStandardItem(data[i][2])
            self.model.appendRow((name, place, born))
        
    def initUI(self):
             
        tv = QtGui.QTreeView(self)
        tv.setRootIsDecorated(False)
        tv.setModel(self.model)
        behavior = QtGui.QAbstractItemView.SelectRows
        tv.setSelectionBehavior(behavior)
        
        self.label = QtGui.QLabel(self)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tv) 
        layout.addWidget(self.label)
        self.setLayout(layout) 
        
        self.connect(tv, QtCore.SIGNAL('clicked(QModelIndex)'), 
            self.onClicked)
        
    def onClicked(self, idx):
        row = idx.row()
        cols = self.model.columnCount()
        
        text = QtCore.QString()
        
        for col in range(cols):
            item = self.model.item(row, col)
            text.append(item.text())
            if col != cols-1:
                text.append(", ")
        
        self.label.setText(text)      
        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()