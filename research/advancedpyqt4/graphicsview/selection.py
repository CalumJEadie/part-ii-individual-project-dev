#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we delete
# selected items from the scene
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: June 2010


from PyQt4 import QtGui, QtCore
              

class View(QtGui.QGraphicsView):
    def __init__(self):
        super(View, self).__init__()
        
        self.setRenderHint(QtGui.QPainter.Antialiasing)
 
        
        
class Scene(QtGui.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        
        self.initScene()
        
    def initScene(self):
        
        for i in range(5):
            
            e = self.addEllipse(20*i, 40*i, 50, 50)
            flag1 = QtGui.QGraphicsItem.ItemIsMovable
            flag2 = QtGui.QGraphicsItem.ItemIsSelectable
            e.setFlag(flag1, True)
            e.setFlag(flag2, True)
                  
        
class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
                
        self.setGeometry(150, 150, 350, 300)
        self.setWindowTitle("Selection")
        
        self.initUI()        
            
    def initUI(self):
    
        hbox = QtGui.QHBoxLayout()
        
        self.view = View()       
        self.scene = Scene()
        self.view.setScene(self.scene)
        
        hbox.addWidget(self.view)
        
        frame = QtGui.QFrame()
        
        self.delete = QtGui.QPushButton("Delete", frame)
        self.delete.setEnabled(False)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.delete)
        vbox.addStretch(1)
        
        frame.setLayout(vbox)
        hbox.addWidget(frame)        
        self.setLayout(hbox)
        
        self.connect(self.delete,
            QtCore.SIGNAL("clicked()"), self.onClick)
        
        self.connect(self.scene, 
            QtCore.SIGNAL("selectionChanged()"), 
            self.selectionChanged)
        
    def onClick(self):

        selectedItems = self.scene.selectedItems()
        
        if len(selectedItems) > 0:
            for item in selectedItems:
                self.scene.removeItem(item)
                
    def selectionChanged(self):
    
        selectedItems = self.scene.selectedItems()
        if len(selectedItems):
            self.delete.setEnabled(True)
        else:
            self.delete.setEnabled(False)

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
