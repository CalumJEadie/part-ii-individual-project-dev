#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# Testing features of a database driver
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: October 2009


from PyQt4 import QtSql, QtCore

app = QtCore.QCoreApplication([])
      
db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
 
driver = db.driver()
print driver.hasFeature(QtSql.QSqlDriver.Transactions)
print driver.hasFeature(QtSql.QSqlDriver.BLOB)
print driver.hasFeature(QtSql.QSqlDriver.Unicode)
print driver.hasFeature(QtSql.QSqlDriver.MultipleResultSets)
print driver.hasFeature(QtSql.QSqlDriver.QuerySize)


                

