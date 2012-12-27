# Adaptation of Button onto Widget

import sys
from PySide import QtGui, QtCore

class Button(QtGui.QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != QtCore.Qt.RightButton:
            return

        mimeData = QtCore.QMimeData()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)


    def mousePressEvent(self, e):
      
        QtGui.QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print 'press'
        

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
    
        self.setAcceptDrops(True)

        self.btn = Button('Button', self)
        self.btn.move(100, 65)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Click or move')
        self.show()

    def dragEnterEvent(self, e):
      
        e.accept()

    def dropEvent(self, e):

        position = e.pos()
        self.btn.move(position)

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()