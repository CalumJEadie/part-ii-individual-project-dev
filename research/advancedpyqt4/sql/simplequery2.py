#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# Doing simple query II
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
    query = QtSql.QSqlQuery("SELECT name, age FROM friends")
    
    query.first()
    name = query.value(0).toString()
    age = query.value(1).toString()
    print name, age

    query.next()
    name = query.value(0).toString()
    age = query.value(1).toString()
    print name, age

    query.last()
    name = query.value(0).toString()
    age = query.value(1).toString()
    print name, age
    
    query.previous()
    name = query.value(0).toString()
    age = query.value(1).toString()
    print name, age







    
