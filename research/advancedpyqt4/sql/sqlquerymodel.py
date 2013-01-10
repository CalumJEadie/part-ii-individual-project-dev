#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we show data from
# a database in a QTableView
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: July 2010


from PyQt4 import QtGui, QtCore, QtSql
      

class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        
        self.move(300, 300)
        self.setWindowTitle("QSqlQueryModel")
       
        self.createConnection()
        self.createModel()
        self.initUI()
        
        self.statusBar().showMessage("Ready")
        

    def onClicked(self, index):
        self.statusBar().showMessage(index.data().toString())

    
    def createConnection(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("friends.db")
        if not db.open():
            print "cannot establish a database connection"
            return False
    
            
    def createModel(self):
    
        self.model = QtSql.QSqlQueryModel()
        query = QtSql.QSqlQuery()
        query.exec_("select * from Friends")

        self.model.setQuery(query)
        self.model.removeColumn(0)
                
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, 
            QtCore.QVariant("Name"))
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, 
            QtCore.QVariant("Age"))
        
    def initUI(self):
    
        self.view = QtGui.QTableView()
        self.view.setModel(self.model)
        
        mode = QtGui.QAbstractItemView.SingleSelection
        self.view.setSelectionMode(mode)
        
        self.connect(self.view, 
            QtCore.SIGNAL('clicked(QModelIndex)'), 
            self.onClicked)
                
        self.setCentralWidget(self.view) 

        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
