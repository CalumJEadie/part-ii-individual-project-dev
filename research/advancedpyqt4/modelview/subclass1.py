#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a read-only
# QAbstractListModel subclass
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: May 2010


from PyQt4 import QtGui, QtCore
      

class MyListModel(QtCore.QAbstractListModel):
    def __init__(self, lang):
        super(MyListModel, self).__init__()
        
        self.lang = lang
        
    def data(self, index, role): 
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.lang[index.row()])
        else: 
            return QtCore.QVariant()    
        
    def rowCount(self, index=QtCore.QModelIndex()): 
        return len(self.lang) 
        
    def flags(self, index):
        fg1 = QtCore.Qt.ItemIsEnabled
        fg2 = QtCore.Qt.ItemIsSelectable 
        return fg1 | fg2 
 


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 250, 200)
        self.setWindowTitle("Subclassing")
       
        self.initData()
        self.initUI()
        
    def initData(self):
    
        languages = ("Python", "Ruby", "Java", 
                    "C", "C#", "C++")
        
        self.model = MyListModel(languages)
            
        
    def initUI(self):
    
        lv = QtGui.QListView(self)
        lv.setModel(self.model)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(lv) 
        self.setLayout(layout) 
        


app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
