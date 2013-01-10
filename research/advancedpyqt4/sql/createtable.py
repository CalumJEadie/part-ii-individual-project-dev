#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# This example creates a table
# and fills it with some data
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
    
    query = QtSql.QSqlQuery("CREATE TABLE Friends("
        "id int primary key, name varchar(20), age int)")
    query.exec_("INSERT INTO Friends VALUES(1,'Tony',15)")
    query.exec_("INSERT INTO Friends VALUES(2,'Bob',28)")
    query.exec_("INSERT INTO Friends VALUES(3,'Isabelle',17)")
    query.exec_("INSERT INTO Friends VALUES(4,'Jane',19)")
    query.exec_("INSERT INTO Friends VALUES(5,'Frank',45)")