#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we group items
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui, QtCore
              

            
class MyGroup(QtGui.QGraphicsItemGroup):
    def __init__(self):
        super(MyGroup, self).__init__()
        
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, 
            True)
    
    def paint(self, painter, option, widget):
    
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        brush = QtGui.QBrush(QtGui.QColor("#333333"))
        pen = QtGui.QPen(brush, 0.5)
        pen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(pen)
        
        if self.isSelected():
            boundRect = self.boundingRect()
            painter.drawRect(boundRect)
        
            

class Scene(QtGui.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        
        
        self.initScene()
        
        
    def initScene(self):    
        
        self.r1 = self.addRect(20, 50, 120, 50)
        self.r1.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.r1.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, 
            True)
        
        self.r2 = self.addRect(150, 100, 50, 50)
        self.r2.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.r2.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, 
            True)

        self.c = self.addEllipse(30, 150, 60, 60)
        self.c.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.c.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, 
            True)
        

class View(QtGui.QGraphicsView):
    def __init__(self):
        super(View, self).__init__()
        
        self.setGeometry(300, 300, 300, 300)
        
        policy = QtCore.Qt.ScrollBarAlwaysOff
        self.setVerticalScrollBarPolicy(policy)
        self.setHorizontalScrollBarPolicy(policy)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
       
        self.init()
        
        
    def init(self):
          
        self.group = None  
        self.scene = Scene()
        self.setSceneRect(0, 0, 300, 300)    
        self.setScene(self.scene)  
        
    def keyPressEvent(self, event): 
           
        key = event.key() 
        
        if key == QtCore.Qt.Key_U:
            if self.group != None and self.group.isSelected():
                items = self.group.childItems()
                self.scene.destroyItemGroup(self.group)
                self.group = None
               
                for item in items:
                    item.setSelected(False)
        
        if key == QtCore.Qt.Key_G:
            if self.group:
                return
                
            selectedItems = self.scene.selectedItems()
            
            if len(selectedItems) > 0:
                self.group = MyGroup()
                
                for item in selectedItems:
                    self.group.addToGroup(item)
                
                self.scene.addItem(self.group)

        
class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        
        hbox = QtGui.QHBoxLayout()
        
        self.view = View()       
        hbox.addWidget(self.view)
        
        self.setLayout(hbox)
        self.setWindowTitle("Group")
        self.setGeometry(250, 150, 300, 300)
        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()