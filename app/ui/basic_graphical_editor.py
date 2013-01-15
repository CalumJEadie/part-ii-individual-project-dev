from PySide import QtGui, QtCore
import os.path
from os.path import join

from ui import language
from interpreter import interpreter

class BasicGraphicalEditor(QtGui.QMainWindow):
    
    def __init__(self):

        super(BasicGraphicalEditor, self).__init__()

        titles = []
        titles.append("Display video title")
        titles.append("Display video description")
        titles.append("Play video")
        titles.append("Ask for user feedback")

        self._model = QtGui.QStringListModel(titles)

        self.setupUI()
        self.show()
        
    def setupUI(self):               
        
        self.setupWindow()
        self.setupToolbar()
        self.setupCentralWidget()
        self.statusBar()

    def setupCentralWidget(self):

        centralWidget = QtGui.QWidget(self)

        hBox = QtGui.QHBoxLayout(centralWidget)

        # hBox.addStretch(50)
        hBox.addWidget(self.createActWidget(centralWidget, self._model))
        # hBox.addStretch(50)

        centralWidget.setLayout(hBox)
        self.setCentralWidget(centralWidget)
         
    def createActWidget(self, parent, model):
        """
        :type parent: QWidget
        :rtype: QWidget:
        """
        # return QtGui.QLabel("ActWidget", parent)
        actWidget = language.ActWidget(parent)
        actWidget.setModel(model)

    def setupToolbar(self):

        toolbar = self.addToolBar('Tools')

        runAction = QtGui.QAction('Run', self)
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip('Run Program')
        runAction.triggered.connect(self.run)
        toolbar.addAction(runAction)

        clearAction = QtGui.QAction('Clear', self)
        clearAction.setShortcut('Ctrl+E')
        clearAction.setStatusTip('Clear Program')
        clearAction.triggered.connect(self.clear)
        toolbar.addAction(clearAction)

        loadExample1Action = QtGui.QAction('Load Example 1', self)
        loadExample1Action.setStatusTip('Replace current program with example 1')
        loadExample1Action.triggered.connect(self.loadExample1)
        toolbar.addAction(loadExample1Action)

        loadExample2Action = QtGui.QAction('Load Example 2', self)
        loadExample2Action.setStatusTip('Replace current program with example 2')
        loadExample2Action.triggered.connect(self.loadExample2)
        toolbar.addAction(loadExample2Action)

    def setupWindow(self):
        self.resize(1024,800)
        self.center()
        self.setWindowTitle('Basic Graphical Editor')
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def loadExample1(self):
        raise NotImplementedError()

    def loadExample2(self):
        raise NotImplementedError()
