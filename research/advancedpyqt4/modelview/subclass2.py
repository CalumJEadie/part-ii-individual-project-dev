#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create an editable
# QAbstractListModel subclass
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: September 2009


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
    
    def setData(self, index, value, role):
        
        val = value.toString()
    
        if val.isEmpty() or not index.isValid():
            return False
            
        if role == QtCore.Qt.EditRole:
                    
            self.lang[index.row()] = value.toString()
            signal = "dataChanged(QModelIndex,QModelIndex)"
            self.emit(QtCore.SIGNAL(signal), 
                       index, index)
            return True
            
        else: return False
            
        
    def rowCount(self, index=QtCore.QModelIndex()): 
    
        return len(self.lang) 
        
    def flags(self, index):
    
        fg1 = QtCore.Qt.ItemIsEnabled
        fg2 = QtCore.Qt.ItemIsSelectable 
        fg3 = QtCore.Qt.ItemIsEditable
        
        return fg1 | fg2 | fg3    
        
    

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 250, 200)
        self.setWindowTitle("Subclass")
       
        self.initUI()
        
        
    def initUI(self):
    
        languages = ["Python", "Ruby", "Java", 
            "C", "C#", "C++"]
        
        self.model = MyListModel(languages)

        lv = QtGui.QListView(self)
        lv.setModel(self.model)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(lv) 
        self.setLayout(layout) 
        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
