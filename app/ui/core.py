"""
Core UI.
"""

from PySide import QtGui, QtCore

class FullscreenDialog(object):

    def fullscreen(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()

class FullscreenDisplayDialog(QtGui.QWidget,FullscreenDialog):
    
    def __init__(self,text):

        super(FullscreenDisplayDialog, self).__init__()
        self.setupUI(text)
        self.show()

    def setupUI(self,text):

        grid_layout = QtGui.QGridLayout(self)

        message_label = QtGui.QLabel(text,self)
        message_label.setAlignment(QtCore.Qt.AlignCenter)
        message_label.setWordWrap(True)
        message_label.setMargin(200)
        font = QtGui.QFont("serif",80)
        message_label.setFont(font)

        grid_layout.addWidget(message_label)

        self.setLayout(grid_layout)

        self.setStyleSheet("background: black; color: white;")

        self.fullscreen()

class FullscreenBooleanDialog(QtGui.QDialog,FullscreenDialog):
    
    def __init__(self,text):

        super(FullscreenBooleanDialog, self).__init__()
        self.setupUI(text)
        self.show()

    def setupUI(self,text):

        grid_layout = QtGui.QGridLayout(self)
        self.setLayout(grid_layout)

        self.setStyleSheet("background: black; color: white;")
        self.fullscreen()        

        # Message
        message_label = QtGui.QLabel(text,self)
        message_label.setAlignment(QtCore.Qt.AlignCenter)
        message_label.setWordWrap(True)
        message_label.setMargin(200)
        font = QtGui.QFont("serif",80)
        message_label.setFont(font)

        grid_layout.addWidget(message_label,0,0,1,2)

        font = QtGui.QFont() # Use default font.
        font.setPointSize(80) # Use large buttons.

        # Yes button
        yes_button = QtGui.QPushButton("&Yes",self)
        yes_button.setFont(font)
        # Connect clicked signal from button to accept virtual function of the dialog.
        yes_button.clicked.connect(self.accept)
        yes_button.setStyleSheet("margin: 100px; padding: 50px; border: 2px solid white;");
        grid_layout.addWidget(yes_button,1,0)

        # No button
        no_button = QtGui.QPushButton("&No",self)
        no_button.setFont(font)
        no_button.clicked.connect(self.reject)
        no_button.setStyleSheet("margin: 100px; padding: 50px; border: 2px solid white;");
        grid_layout.addWidget(no_button,1,1)

    @classmethod
    def getBoolean(cls,text):
        """
        Static convenience method. Modelled after similiar methods in concrete
        subclasses of QDialog in PySide, such as QInputDialog.getString()

        :rtype: boolean
        """
        dialog = cls(text)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            return True
        else:
            return False


class VerticallyGrowingPlainTextEdit(QtGui.QPlainTextEdit):
    """
    Based on http://stackoverflow.com/questions/11677499/pyside-qt-auto-vertical-growth-for-textedit-widget-and-spacing-between-widgets.
    """

    def __init__(self, text, parent=None):
        super(VerticallyGrowingPlainTextEdit, self).__init__(text, parent)

        self.document().contentsChanged.connect(self.sizeChange)

        self._heightMin = 0
        self._heightMax = 65000

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self._heightMin <= docHeight <= self._heightMax:
            self.setMinimumHeight(docHeight)