from PySide.QtCore import *
from PySide.QtGui import *
import os.path
from os.path import join

from app.ui.language import *
from app.interpreter import interpreter

class GraphicalEditor(QMainWindow):

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

        centralwidget = QWidget(self)

        horizontalLayout = QHBoxLayout(centralwidget)

        # Add toolbar and editor pane
        
        horizontalLayout.addWidget(self.createSidebar(centralwidget))
        horizontalLayout.addWidget(self.createEditorPane(centralwidget))

        self.setCentralWidget(centralwidget)

    def createSidebar(self, parent):
        """
        type parent: QWidget
        :rtype: QWidget
        """

        sceneBox = QGroupBox("Scenes")
        sceneBoxLayout = QVBoxLayout()
        sceneBoxLayout.addWidget(SceneWidget())
        sceneBox.setLayout(sceneBoxLayout)

        videoBox = QGroupBox("Video and Video Collections")
        videoBoxLayout = QVBoxLayout()
        videoBoxLayout.addWidget(VideoDefnWidget())
        videoBoxLayout.addWidget(VideoCollectionDefnWidget())
        videoBox.setLayout(videoBoxLayout)

        textBox = QGroupBox("Text")
        textBoxLayout = QVBoxLayout()
        textBoxLayout.addWidget(TextValueWidget())
        textBox.setLayout(textBoxLayout)

        numberBox = QGroupBox("Numbers")
        numberBoxLayout = QVBoxLayout()
        numberBoxLayout.addWidget(NumberValueWidget())
        numberBox.setLayout(numberBoxLayout)

        variableBox = QGroupBox("Variables")
        variableBoxLayout = QVBoxLayout()
        variableBoxLayout.addWidget(GetterWidget())
        variableBoxLayout.addWidget(SetterWidget())
        variableBox.setLayout(variableBoxLayout)

        sidebar = QWidget()
        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(sceneBox)
        sidebarLayout.addWidget(videoBox)
        sidebarLayout.addWidget(textBox)
        sidebarLayout.addWidget(numberBox)
        sidebarLayout.addWidget(variableBox)
        sidebarLayout.addStretch()
        sidebar.setLayout(sidebarLayout)

        sidebar.setFixedWidth(300)

        return sidebar

    def createToolbox(self,parent):
        """
        :type parent: QWidget
        :rtype: QWidget
        """

        toolBox = QToolBox(parent)
        toolBox.setMaximumSize(QSize(300, 16777215))
        # self.toolBox.setCurrentIndex(0)

        # Scenes
        page_3 = QWidget()
        page_3.setGeometry(QRect(0, 0, 300, 438))
        SceneWidget(page_3)
        toolBox.addItem(page_3, "Scenes")


        # Videos and Video Collections
        page_4 = QWidget()
        page_4.setGeometry(QRect(0, 0, 300, 438))
        widget_3 = VideoDefnWidget(page_4)
        widget_4 = VideoCollectionDefnWidget(page_4)
        toolBox.addItem(page_4, "Videos and Video Collections")

        # Variables
        page_5 = QWidget()
        verticalLayout = QVBoxLayout(page_5)
        widget = SetterWidget(page_5)
        widget_2 = GetterWidget(page_5)
        verticalLayout.addWidget(widget)
        verticalLayout.addWidget(widget_2)
        page_5.setLayout(verticalLayout)
        toolBox.addItem(page_5, "Variables")

        return toolBox

    def createEditorPane(self,parent):
        """
        :type parent: QWidget
        :rtype: QWidget
        """

        editorPaneLayout = QHBoxLayout()

        actWidget = ActWidget()

        # Create stretchable space either side of act.
        editorPaneLayout.addStretch(50)
        editorPaneLayout.addWidget(actWidget)
        editorPaneLayout.addStretch(50)

        editorPane = QWidget(parent)
        editorPane.setLayout(editorPaneLayout)

        return editorPane

    def setupToolbar(self):

        runAction = QAction('Run', self)
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip('Run Program')
        runAction.triggered.connect(self.run)

        clearAction = QAction('Clear', self)
        clearAction.setShortcut('Ctrl+E')
        clearAction.setStatusTip('Clear Program')
        clearAction.triggered.connect(self.clear)

        loadExample1Action = QAction('Load Example 1', self)
        loadExample1Action.setStatusTip('Replace current program with example 1')
        loadExample1Action.triggered.connect(self.loadExample1)

        loadExample2Action = QAction('Load Example 2', self)
        loadExample2Action.setStatusTip('Replace current program with example 2')
        loadExample2Action.triggered.connect(self.loadExample2)

        toolbar = self.addToolBar('Tools')
        toolbar.addAction(runAction)
        toolbar.addAction(clearAction)
        toolbar.addAction(loadExample1Action)
        toolbar.addAction(loadExample2Action)

    def setupWindow(self):

        self.resize(1200,800)
        self.center()
        self.setWindowTitle('Graphical Editor')
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
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
