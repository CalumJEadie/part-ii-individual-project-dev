"""
Core UI.
"""

from PySide import QtGui, QtCore

from app.ui import events

class FullscreenDialog(object):

    def fullscreen(self):
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)
        # self.setWindowFlags(QtCore.Qt.Window)

        # self.setWindowState(QtCore.Qt.WindowFullScreen)
        
        self.showFullScreen()

# class FullscreenDisplayDialog(QtGui.QWidget,FullscreenDialog):
    
#     def __init__(self,text):

#         super(FullscreenDisplayDialog, self).__init__()
#         self.setupUI(text)
#         self.show()

#     def setupUI(self,text):

#         grid_layout = QtGui.QGridLayout(self)

#         message_label = QtGui.QLabel(text,self)
#         message_label.setAlignment(QtCore.Qt.AlignCenter)
#         message_label.setWordWrap(True)
#         message_label.setMargin(200)
#         font = QtGui.QFont("serif",80)
#         message_label.setFont(font)

#         grid_layout.addWidget(message_label)

#         self.setLayout(grid_layout)

#         self.setStyleSheet("background: black; color: white;")

#         self.fullscreen()

class FullscreenDisplayDialog(QtGui.QDialog,FullscreenDialog):
    
    def __init__(self,text):

        super(FullscreenDisplayDialog, self).__init__()
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

    @classmethod
    def display(cls, text, duration):
        """
        Static convenience method. Display text for duration seconds.
        """
        dialog = cls(text)
        QtCore.QTimer.singleShot(duration*1000, dialog.close)
        dialog.exec_()

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

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.document().contentsChanged.connect(self._sizeChange)

    def _sizeChange(self):
        # Need to get font at size change event as CSS not applied at __init__.
        fm = QtGui.QFontMetrics(self.font())

        # Adjust for line spacing.
        lineHeight = fm.height() * 1.4
        numLines = self.document().size().height()
        self.setMinimumHeight(numLines * lineHeight)

class HGrowingLineEdit(QtGui.QLineEdit):

    minVisibleLength = 6
    maxVisibleLength = 30

    def __init__(self, text, parent=None):
        super(HGrowingLineEdit, self).__init__(text, parent)
        # Need to notify layout when size has changed.
        self.textChanged.connect(self.updateGeometry)
        # sizeHint is the only acceptable size.
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        # Make sure that at least minVisibleLength characters can be seen
        # and at most maxVisibleLength
        contentsWidth = fm.width(self.text())+10
        width = max(self.minVisibleLength * fm.averageCharWidth(), contentsWidth)
        width = min(width, self.maxVisibleLength * fm.averageCharWidth())
        return QtCore.QSize(width, self.minimumHeight())

class Application(QtGui.QApplication):
    """
    Reimplementation that can propogate custom events.

    Based on http://stackoverflow.com/questions/3180506/propagate-custom-qevent-to-parent-widget-in-qt-pyqt.
    """

    def notify(self, receiver, event):
        if event.type() > QtCore.QEvent.User:
            w = receiver
            while(w):
                # Note that this calls `event` method directly thus bypassing
                # calling qApplications and receivers event filters
                res = w.event(event)
                if res and event.isAccepted():
                    return res
                w = w.parent()
        return super(Application, self).notify(receiver, event)