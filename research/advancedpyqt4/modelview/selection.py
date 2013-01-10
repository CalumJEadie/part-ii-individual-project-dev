#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we calculate
# the sum of numbers in the QTableView
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui, QtCore
   

class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("Selection")
       
        self.initData()
        self.initUI()
        
        
    def initUI(self):
             
        self.tv = QtGui.QTableView(self)
        self.tv.setModel(self.model)
        icon = QtGui.QIcon('sum.png')
        self.nsum = QtGui.QAction(icon, 'Sum', self)
        self.nsum.setShortcut('Ctrl+Q')
        self.connect(self.nsum, QtCore.SIGNAL('triggered()'), 
                      self.onClicked)
        
        self.toolbar = self.addToolBar('Sum')
        self.toolbar.addAction(self.nsum)

        self.setCentralWidget(self.tv) 
        
    
    def onClicked(self):
        
        nsum = 0
    
        selmod = self.tv.selectionModel()
        selection = selmod.selection()
        indexes = selection.indexes()
        
        for idx in indexes:
            num = idx.data().toInt()
            nsum += num[0]
        
        lastIndex = indexes[-1]
        r, c = lastIndex.row(), lastIndex.column()
    
        item = QtGui.QStandardItem(str((nsum)))
        self.model.setItem(r+1, c, item)
                          
    def initData(self):
        self.model = QtGui.QStandardItemModel(15, 15)
 
        
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
