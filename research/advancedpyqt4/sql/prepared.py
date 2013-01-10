#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we show, how to create 
# prepared statements
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtCore, QtSql


app = QtCore.QCoreApplication([])
      
db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("friends.db")
 

if not db.open():
    print "cannot establish a database connection"

else: 
    
    query = QtSql.QSqlQuery("INSERT INTO friends("
        "id, name, age) VALUES (?, ?, ?)")
    query.bindValue(0, QtCore.QVariant(6))
    query.bindValue(1, QtCore.QVariant("Monika"))
    query.bindValue(2, QtCore.QVariant(23))
    query.exec_()
    
    query = QtSql.QSqlQuery("SELECT name, age FROM friends")
    query.last()
    
    name = query.value(0).toString()
    age = query.value(1).toString()
    print name, age
