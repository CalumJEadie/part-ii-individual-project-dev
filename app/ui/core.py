"""
Core UI.
"""

from PySide import QtGui, QtCore

class FullscreenDisplayDialogue(QtGui.QWidget):
    
    def __init__(self,text):

        super(FullscreenDisplayDialogue, self).__init__()
        self.setupUI(text)
        self.show()

    def setupUI(self,text):

        grid = QtGui.QGridLayout(self)

        label = QtGui.QLabel(text,self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        label.setMargin(200)
        font = QtGui.QFont("serif",40)
        label.setFont(font)

        grid.addWidget(label)

        self.setLayout(grid)

        self.setStyleSheet("background: black; color: white;")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()