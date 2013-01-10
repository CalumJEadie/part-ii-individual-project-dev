#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a grayscale image
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2010


from PyQt4 import QtGui


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initExample()

        self.setGeometry(200, 200, 320, 150)
        self.setWindowTitle('Sid')

        
    def initExample(self):
        self.sid = QtGui.QImage("smallsid.jpg")

        self.w = self.sid.width()
        self.h = self.sid.height()
       

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawImages(painter)
        painter.end()
        
    def grayScale(self, image):
        
        for i in range(self.w):
            for j in range(self.h):
                c = image.pixel(i, j)
                gray = QtGui.qGray(c)
                alpha = QtGui.qAlpha(c)
                image.setPixel(i, j, 
                      QtGui.qRgba(gray, gray, gray, alpha))
          
        return image

        

    def drawImages(self, painter):
    
        painter.drawImage(5, 15, self.sid)
        painter.drawImage(self.w+10, 15,
                           self.grayScale(self.sid.copy()))
      
       
app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()