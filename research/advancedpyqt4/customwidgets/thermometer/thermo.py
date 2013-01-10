#!/usr/bin/python

# ZetCode Advanced PyQt4 tutorial 
#
# In this example, we create a custom 
# Thermometer widget
#
# original author: Tomasz Ziobrowski
# adopted by: Jan Bodnar
# website: zetcode.com 
# last edited: May 2010


from PyQt4 import QtGui, QtCore

OFFSET = 10
SCALE_HEIGHT = 224

class Thermometer(QtGui.QWidget):
    def __init__(self, parent):
        super(Thermometer, self).__init__()

        self.value = 0
        
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.initDrawing(painter)
        self.drawTemperature(painter)
        self.drawBackground(painter)
        painter.end()
  

    def initDrawing(self, painter):
    
        self.normal = 25.0
        self.critical = 75.0
        self.m_min = 0.0
        self.m_max = 80.0

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width()/2.0, 0.0)
        painter.scale(self.height()/300.0, 
                       self.height()/300.0)
        
        
    def drawBackground(self, painter):

        path = QtGui.QPainterPath()

        path.moveTo(-7.5, 257.0)
        path.quadTo(-12.5, 263.0, -12.5, 267.5)
        path.quadTo(-12.5, 278.0, 0.0, 280.0)
        path.quadTo(12.5, 278.0, 12.5, 267.5)
        path.moveTo(12.5, 267.5) 
        path.quadTo(12.5, 263.0, 7.5, 257.0) 
        
        path.lineTo(7.5, 25.0)
        path.quadTo(7.5, 12.5, 0, 12.5)
        path.quadTo(-7.5, 12.5, -7.5, 25.0)
        path.lineTo(-7.5, 257.0)
        
        p1 = QtCore.QPointF(-2.0, 0.0)
        p2 = QtCore.QPointF(12.5, 0.0)
        linearGrad = QtGui.QLinearGradient(p1, p2)
        linearGrad.setSpread(QtGui.QGradient.ReflectSpread)
        linearGrad.setColorAt(1.0, 
            QtGui.QColor(0, 150, 255, 170))
        linearGrad.setColorAt(0.0, 
            QtGui.QColor(255, 255, 255, 0))

        painter.setBrush(QtGui.QBrush(linearGrad))
        painter.setPen(QtCore.Qt.black)
        painter.drawPath(path)
        
        pen = QtGui.QPen()
        length = 12
                
        for i in range(33):
            
            pen.setWidthF(1.0)
            length = 12
            
            if i % 4:
                length = 8 
                pen.setWidthF(0.8)
                
            if i % 2:
                length = 5
                pen.setWidthF(0.6)
                
            painter.setPen(pen)
            painter.drawLine(-7, 28+i*7, -7+length, 28+i*7)
        
        for i in range(9):    
            
            num = self.m_min + i*(self.m_max-self.m_min)/8.0
            val = QtCore.QString("%1").arg(num)
            fm = painter.fontMetrics()
            size = fm.size(QtCore.Qt.TextSingleLine, val)
            point = QtCore.QPointF(OFFSET, 
                        252-i*28+size.width()/4.0)
            painter.drawText(point, val)
    
    
    def drawTemperature(self, painter):

        if self.value >= self.critical:
            color = QtGui.QColor(255, 0, 0) 
     
        elif self.value >= self.normal:
            color = QtGui.QColor(0, 200, 0)
        
        else:
            color = QtGui.QColor(0, 0, 255)
            
        scale = QtGui.QLinearGradient(0.0, 0.0, 5.0, 0.0)
        bulb = QtGui.QRadialGradient(0.0, 267.0, 
                                      10.0, -5.0, 262.0)

        scale.setSpread(QtGui.QGradient.ReflectSpread)
        bulb.setSpread(QtGui.QGradient.ReflectSpread)

        color.setHsv(color.hue(), color.saturation(),
                      color.value())
        scale.setColorAt(1.0, color)
        bulb.setColorAt(1.0, color)

        color.setHsv(color.hue(), color.saturation()-200, 
            color.value())
        scale.setColorAt(0.0, color)
        bulb.setColorAt(0.0, color)

        factor = self.value-self.m_min 
        factor = (factor/self.m_max)-self.m_min

        temp = SCALE_HEIGHT * factor
        height = temp + OFFSET
        
        
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(scale)
        painter.drawRect(-5, 252+OFFSET-height, 10, height)
        painter.setBrush(bulb)
        rect = QtCore.QRectF(-10.0, 258, 20.0, 20.0)
        painter.drawEllipse(rect)
        

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.setGeometry(300, 100, 250, 350)
        self.setWindowTitle('Thermometer')
        
        self.initUI()
        
        
    def initUI(self):
        
        self.value = 0
        
        vbox = QtGui.QVBoxLayout()
        
        self.the = Thermometer(self)
        vbox.addWidget(self.the)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        vbox.addWidget(self.slider)
        self.slider.setMaximum(80)
        
        self.connect(self.slider, 
            QtCore.SIGNAL('valueChanged(int)'), self.changeVal)

        self.setLayout(vbox)
       
    def changeVal(self):
        self.the.value = self.slider.value()
        self.the.repaint()
 

app = QtGui.QApplication([])
ex = Example()
ex.show()
app.exec_()
