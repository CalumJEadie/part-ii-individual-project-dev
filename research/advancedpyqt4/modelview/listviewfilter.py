#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we filter items in 
# a QListView using a QSortFilterProxyModel class
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: May 2010


from PyQt4 import QtGui, QtCore
      

FIRST_COLUMN = 0


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 400, 240)
        self.setWindowTitle("Filtering data")
       
        self.initData()
        self.initUI()
        
    def initData(self):
    
        words = QtCore.QStringList()
        words.append("radar")
        words.append("Robert")
        words.append("Rome")
        words.append("rodeo")
        words.append("rust")
        words.append("ready")
        words.append("robot")
        words.append("rampart")
        words.append("RAM")
        words.append("ROM")
        
        self.model = QtGui.QStringListModel(words)
        self.filterModel = QtGui.QSortFilterProxyModel(self)
        self.filterModel.setSourceModel(self.model)
        self.filterModel.setDynamicSortFilter(True)
        
    
    def initUI(self):
    
    
        self.filterText = QtGui.QLineEdit(self)
        self.filterText.move(250, 20)
        

    
        self.case = QtGui.QCheckBox("Case sensitive", self)
        self.case.move(250, 70)
    
        self.filterCb = QtGui.QComboBox(self)
        self.filterCb.addItem("Regular expression",
            QtCore.QVariant(QtCore.QRegExp.RegExp))
        self.filterCb.addItem("Wildcard", 
            QtCore.QVariant(QtCore.QRegExp.Wildcard))
        self.filterCb.addItem("Fixed string",
            QtCore.QVariant(QtCore.QRegExp.FixedString))
        self.filterCb.move(20, 190)
        
        
        self.connect(self.filterCb, 
            QtCore.SIGNAL('activated(const QString &)'), 
            self.filterItems)
        
        self.connect(self.filterText, 
            QtCore.SIGNAL('textChanged(const QString &)'), 
            self.filterItems)
        
        self.connect(self.case, QtCore.SIGNAL('toggled(bool)'), 
            self.filterItems)
    
        
        self.lv = QtGui.QListView(self)
        self.lv.setModel(self.filterModel)
        self.lv.setGeometry(20, 20, 200, 150)
        
        
    def filterItems(self, value):
        
        idx = self.filterCb.currentIndex()
        syntaxType, _ = self.filterCb.itemData(idx).toInt()
        syntax = QtCore.QRegExp.PatternSyntax(syntaxType)
        
        if self.case.isChecked():
            case = QtCore.Qt.CaseSensitive
        else:
            case = QtCore.Qt.CaseInsensitive
        
        regExp = QtCore.QRegExp(self.filterText.text(), 
                                 case, syntax)
        self.filterModel.setFilterRegExp(regExp)

        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
