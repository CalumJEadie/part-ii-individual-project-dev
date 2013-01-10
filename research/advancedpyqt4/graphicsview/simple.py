#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# This is a simple example of the
# Graphics View framework
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: June 2010


from PyQt4 import QtGui, QtCore
      
        

class Example(QtGui.QGraphicsView):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Simple")
       
        self.init()
        
        
    def init(self):

        self.scene = QtGui.QGraphicsScene()
        
        self.scene.addText("ZetCode")
        self.setScene(self.scene)        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()



