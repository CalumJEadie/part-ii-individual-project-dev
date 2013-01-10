#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we draw basic
# shapes
#
# author: Jan Bodnar
# website: zetcode.com 
# last edited: April 2009


from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.setGeometry(300, 300, 350, 280)
        self.setWindowTitle('Shapes')

    def paintEvent(self, event):
    
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawShapes(painter)
        painter.end()
        
    def drawShapes(self, painter):

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#888888")))

        path1 = QtGui.QPainterPath()

        path1.moveTo(5, 5)
        path1.cubicTo(40, 5,  50, 50,  99, 99)
        path1.cubicTo(5, 99,  50, 50,  5, 5)
        painter.drawPath(path1)

        painter.drawPie(130, 20, 90, 60, 30*16, 120*16)
        painter.drawChord(240, 30, 90, 60, 0, 16*180)
        painter.drawRoundRect(20, 120, 80, 50)

        polygon = QtGui.QPolygon()
        polygon.append(QtCore.QPoint(130, 140))
        polygon.append(QtCore.QPoint(180, 170))
        polygon.append(QtCore.QPoint(180, 140))
        polygon.append(QtCore.QPoint(220, 110))
        polygon.append(QtCore.QPoint(140, 100))
                
        painter.drawPolygon(polygon)

        painter.drawRect(250, 110, 60, 60)

        baseline = QtCore.QPointF(20, 250)
        font = QtGui.QFont("Georgia", 55)
        path2 = QtGui.QPainterPath()
        path2.addText(baseline, font, "Q")
        painter.drawPath(path2)

        painter.drawEllipse(140, 200, 60, 60)
        painter.drawEllipse(240, 200, 90, 60)

    

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()