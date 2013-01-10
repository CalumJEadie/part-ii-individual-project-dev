#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a custom 
# graphics item based on a QGraphicsRectItem
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: June 2010


from PyQt4 import QtGui, QtCore
      

class Item(QtGui.QGraphicsRectItem):
    def __init__(self,x,y,w,h):
        super(Item, self).__init__(x, y, w, h)
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setCursor(QtCore.Qt.SizeAllCursor)
        self.setBrush(QtGui.QColor(250, 100, 0))
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        

class Example(QtGui.QGraphicsView):
    def __init__(self):
        super(Example, self).__init__()
        
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Custom item")
       
        self.init()
        
        
    def init(self):

        self.scene = QtGui.QGraphicsScene()
        
        self.item = Item(0, 0, 100, 100)
        self.scene.addItem(self.item)
                
        self.setScene(self.scene)        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()



