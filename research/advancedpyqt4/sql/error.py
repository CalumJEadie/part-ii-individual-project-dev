#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we work with an SQL query error
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtSql, QtCore

app = QtCore.QCoreApplication([])
      
db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("friends.db")
 

if not db.open():
    print "cannot establish a database connection"

else: 
    query = QtSql.QSqlQuery("SELECT friend, age FROM Friends")
    while query.next():
        friend = query.value(0).toString()
        age = query.value(1).toString()
        print friend, age

error = query.lastError()
print error.text()
    
