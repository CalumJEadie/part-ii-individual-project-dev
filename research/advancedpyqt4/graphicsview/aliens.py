#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we we will
# avoid and shoot alien ships
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: August 2010


from PyQt4 import QtGui, QtCore
              
DELAY = 10
BOARD_WIDTH = 390
MISSILE_SPEED = 2
CRAFT_SIZE = 20


class Missile(QtGui.QGraphicsPixmapItem):

    def __init__(self, x, y):
        super(Missile, self).__init__()
        self.setPixmap(QtGui.QPixmap('missile.png'))

        self.x = x
        self.y = y
        
        self.setPos(self.x, self.y)
           
    
    def move(self):
    
        self.x += MISSILE_SPEED
        
        if (self.x > BOARD_WIDTH):
            scene = self.scene()
            scene.removeItem(self)
        else: 
            self.setPos(self.x, self.y)
    
    
    
class Alien(QtGui.QGraphicsPixmapItem):

    def __init__(self, x, y):
        super(Alien, self).__init__()
    
        self.x = x
        self.y = y
        
        self.setPixmap(QtGui.QPixmap('alien.png'))
        self.setPos(self.x, self.y)
     
    def move(self):
    
        if self.x < 0:
            self.x = 400
        else:
            self.x = self.x - 1
            self.setPos(self.x, self.y)
    
    
class Craft(QtGui.QGraphicsPixmapItem):

    def __init__(self):
        super(Craft, self).__init__()
        
        self.setPixmap(QtGui.QPixmap('craft.png'))
        self.setPos(50, 50)
        
        self.dx = 0
        self.dy = 0
        
        
    def move(self):
        x, y = self.x(), self.y()
        x += self.dx
        y += self.dy
        self.setPos(x, y)
    
        
    def onKeyPress(self, event): 
      
        key = event.key()    
        
        if key == QtCore.Qt.Key_Left:
            self.dx = -1 
                
        if key == QtCore.Qt.Key_Right: 
            self.dx = 1        
        
        if key == QtCore.Qt.Key_Up: 
            self.dy = -1                      
        
        if key == QtCore.Qt.Key_Down: 
            self.dy = 1   
        
    def onKeyRelease(self, event): 
           
        key = event.key() 
        
        if key == QtCore.Qt.Key_Left:
            self.dx = 0
                
        if key == QtCore.Qt.Key_Right: 
            self.dx = 0        
        
        if key == QtCore.Qt.Key_Up: 
            self.dy = 0                      
        
        if key == QtCore.Qt.Key_Down: 
            self.dy = 0  


class View(QtGui.QGraphicsView):

    def __init__(self):
        super(View, self).__init__()
        
        self.setGeometry(300, 300, 390, 390)
        
        self.setSceneRect(0, 0, 390, 390)
        self.setBackgroundBrush(QtGui.QColor(0, 0, 0))
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        policy = QtCore.Qt.ScrollBarAlwaysOff
        self.setVerticalScrollBarPolicy(policy)
        self.setHorizontalScrollBarPolicy(policy)

       
        self.init()
        
        
    def init(self):
    
        self.pos = ( 
            (2380, 129), (2500, 59), (1380, 89),
            (3780, 109), (580, 139), (680, 239), 
            (790, 259), (760, 150), (790, 150),
            (2930, 159), (590, 80), (530, 60),
            (1900, 259), (2660, 150), (1540, 90),
            (810, 220), (860, 320), (740, 180),
            (820, 128), (490, 170), (700, 230)
        )

        self.naliens = len(self.pos)

        self.scene = QtGui.QGraphicsScene()
        
        self.craft = Craft()
        self.scene.addItem(self.craft)         
        self.setScene(self.scene)  

        for i in range(len(self.pos)):
            alien = Alien(self.pos[i][0], self.pos[i][1])
            self.scene.addItem(alien)
            
        text = "Aliens left: %d" % self.naliens    
        self.score = self.scene.addText(text)
        self.score.setPos(15, 15)
        self.score.setDefaultTextColor(QtCore.Qt.white)
                 
        self.timer = QtCore.QBasicTimer()
        self.timer.start(DELAY, self)   
        
    def timerEvent(self, event):

        self.updateScore()
        self.checkCollisions()
        self.moveItems()
        
    def updateScore(self):
        
        text = "Aliens left: %d" % self.naliens
        
        self.score.setPlainText(text)
        
        
    def fire(self):
        
        if not self.timer.isActive():
            return
        
        missile = Missile(self.craft.x() + CRAFT_SIZE+1, 
            self.craft.y() + CRAFT_SIZE/2)
        self.scene.addItem(missile)  
        
    
    def checkCollisions(self):
        
        if not self.naliens:
            self.gameOver("Game won")
        
        items = self.items()

        
        for i in range(len(items)):
            item = items[i]
            
            col_item = self.scene.collidingItems(item)
            
            if col_item:
                
                if item.collidesWithItem(self.score):
                    continue
  
                if isinstance(item, Craft) or \
                    isinstance(col_item[0], Craft):
      
                    self.gameOver("Game lost")
                    return
                
                if isinstance(item, Alien):
  
                    self.naliens = self.naliens - 1
                    self.scene.removeItem(item) 
                    self.scene.removeItem(col_item[0])
                
    
    def moveItems(self):
        
        items = self.items()
        nItems = len(items)
        
        for i in range(nItems):
            
            item = items[i]
            
            if not isinstance(item, QtGui.QGraphicsTextItem):
                item.move()
         
    def gameOver(self, text):
    
        self.timer.stop()
        self.scene.clear()
        
        textItem = self.scene.addText(text)
        textItem.setDefaultTextColor(QtCore.Qt.white)
        textItem.setPos(50, 50)
        
    
    def keyPressEvent(self, e): 
         
        key = e.key()    

        if key == QtCore.Qt.Key_Space:
            self.fire()
        else:
            self.craft.onKeyPress(e)           
            
    def keyReleaseEvent(self, e): 
          
        self.craft.onKeyRelease(e) 
        
        
        
class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        
        hbox = QtGui.QHBoxLayout()
        
        self.view = View()       
        hbox.addWidget(self.view)
        
        self.setLayout(hbox)
        self.setWindowTitle("Aliens")
        self.setGeometry(250, 150, 390, 390)
        

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()