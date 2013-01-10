from PySide import QtGui, QtCore
import os.path
from os.path import join

from ui import language
from interpreter import interpreter

class GraphicalEditor(QtGui.QMainWindow):

    d = os.path.dirname(__file__)
    example1 = open(join(d,"example1.py")).read()
    example2 = open(join(d,"example2.py")).read()
    
    def __init__(self):

        super(GraphicalEditor, self).__init__()
        self.setupUI()
        self.show()
        
    def setupUI(self):               
        
        self.setupWindow()
        self.setupToolbar()
        self.setupCentralWidget()
        self.statusBar()

    def setupCentralWidget(self):
        
        # Set up layout

        centralwidget = QtGui.QWidget(self)

        horizontalLayout = QtGui.QHBoxLayout(centralwidget)

        # Add toolbar and editor pane
        
        horizontalLayout.addWidget(self.createToolbox(centralwidget))
        horizontalLayout.addWidget(self.createEditorPane(centralwidget))

        self.setCentralWidget(centralwidget)

    def createToolbox(self,parent):
        """
        :type parent: QtGui.QWidget
        :rtype: QtGui.QWidget
        """

        toolBox = QtGui.QToolBox(parent)
        toolBox.setMaximumSize(QtCore.QSize(300, 16777215))
        # self.toolBox.setCurrentIndex(0)

        # Scenes
        page_3 = QtGui.QWidget()
        page_3.setGeometry(QtCore.QRect(0, 0, 300, 438))
        language.SceneWidget(page_3)
        toolBox.addItem(page_3, "Scenes")


        # Videos and Video Collections
        page_4 = QtGui.QWidget()
        page_4.setGeometry(QtCore.QRect(0, 0, 300, 438))
        widget_3 = language.VideoDefnWidget(page_4)
        widget_4 = language.VideoCollectionDefnWidget(page_4)
        toolBox.addItem(page_4, "Videos and Video Collections")

        # Variables
        page_5 = QtGui.QWidget()
        verticalLayout = QtGui.QVBoxLayout(page_5)
        widget = language.SetterWidget(page_5)
        widget_2 = language.GetterWidget(page_5)
        verticalLayout.addWidget(widget)
        verticalLayout.addWidget(widget_2)
        page_5.setLayout(verticalLayout)
        toolBox.addItem(page_5, "Variables")

        return toolBox

    def createEditorPane(self,parent):
        """
        :type parent: QtGui.QWidget
        :rtype: QtGui.QWidget
        """

        editorPane = QtGui.QWidget(parent)

        hBoxLayout = QtGui.QHBoxLayout(editorPane)
        editorPane.setLayout(hBoxLayout)

        scrollArea = QtGui.QScrollArea(editorPane)
        hBoxLayout.addStretch(50) # Create stretchable space either side of act.
        hBoxLayout.addWidget(scrollArea)
        hBoxLayout.addStretch(50) # Create stretchable space either side of act.

        actWidget = QtGui.QWidget(scrollArea)
        actWidget.setMinimumSize(400,400)
        scrollArea.setWidget(actWidget)
        # scrollArea.setWidget(language.SceneWidget())
        # return editorPane

        vBoxLayout = QtGui.QVBoxLayout(actWidget)
        actWidget.setLayout(vBoxLayout)

        for i in range(0,20):
            # sw = language.SceneWidget(actWidget)
            # vBoxLayout.addWidget(sw)
            vBoxLayout.addWidget(QtGui.QLabel("test %s" % i))

        return editorPane

        # scrollArea_2 = QtGui.QScrollArea(parent)
        # scrollArea_2.setWidgetResizable(True)

        # scrollAreaWidgetContents_2 = QtGui.QWidget()
        # scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 582, 538))

        # scrollArea_2.setWidget(scrollAreaWidgetContents_2)

        # return scrollArea_2

    def setupToolbar(self):

        runAction = QtGui.QAction('Run', self)
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip('Run Program')
        runAction.triggered.connect(self.run)

        clearAction = QtGui.QAction('Clear', self)
        clearAction.setShortcut('Ctrl+E')
        clearAction.setStatusTip('Clear Program')
        clearAction.triggered.connect(self.clear)

        loadExample1Action = QtGui.QAction('Load Example 1', self)
        loadExample1Action.setStatusTip('Replace current program with example 1')
        loadExample1Action.triggered.connect(self.loadExample1)

        loadExample2Action = QtGui.QAction('Load Example 2', self)
        loadExample2Action.setStatusTip('Replace current program with example 2')
        loadExample2Action.triggered.connect(self.loadExample2)

        toolbar = self.addToolBar('Tools')
        toolbar.addAction(runAction)
        toolbar.addAction(clearAction)
        toolbar.addAction(loadExample1Action)
        toolbar.addAction(loadExample2Action)

    def setupWindow(self):

        self.resize(1024,800)
        self.center()
        self.setWindowTitle('Graphical Editor')
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run(self):
        program = self.textEdit.toPlainText()
        interpreter.interpret(program)

    def clear(self):
        self.textEdit.clear()

    def loadExample1(self):
        self.textEdit.setPlainText(self.example1)

    def loadExample2(self):
        self.textEdit.setPlainText(self.example2)
