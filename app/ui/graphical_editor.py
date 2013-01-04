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

        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)

        self.horizontalLayout = QtGui.QHBoxLayout()

        # Add toolbar and editor pane
        
        self.setupToolbox()
        self.setupEditorPane()






        

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.setCentralWidget(self.centralwidget)

    def setupToolbox(self):

    
        self.toolBox = QtGui.QToolBox(self.centralwidget)
        self.toolBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.toolBox.setObjectName("toolBox")




        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 300, 438))
        self.page_3.setObjectName("page_3")




        self.scrollArea = QtGui.QScrollArea(self.page_3)
        self.scrollArea.setGeometry(QtCore.QRect(480, 120, 120, 80))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 118, 78))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


        self.widget_5 = language.SceneWidget(self.page_3)
        self.toolBox.addItem(self.page_3, "Scenes")



        self.page_4 = QtGui.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 300, 438))
        self.page_4.setObjectName("page_4")

        self.widget_3 = language.VideoDefnWidget(self.page_4)
        self.widget_4 = language.VideoCollectionDefnWidget(self.page_4)


        self.toolBox.addItem(self.page_4, "Videos and Video Collections")



        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")




        self.toolBox.addItem(self.page_5, "Variables")




        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.page_5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")



        self.widget = language.SetterWidget(self.page_5)
        self.verticalLayout.addWidget(self.widget)


        self.widget_2 = language.GetterWidget()
        self.verticalLayout.addWidget(self.widget_2)

        self.horizontalLayout_7.addLayout(self.verticalLayout)


        self.toolBox.setCurrentIndex(0)





        self.horizontalLayout.addWidget(self.toolBox)

    def setupEditorPane(self):

        self.scrollArea_2 = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")

        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 582, 538))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout.addWidget(self.scrollArea_2)

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
