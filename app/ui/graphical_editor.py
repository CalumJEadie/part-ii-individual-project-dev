from PySide.QtCore import *
from PySide.QtGui import *
import os.path
from os.path import join
import logging

from app.ui.language import *
from app.interpreter import interpreter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        
        horizontalLayout.addWidget(PaletteWidget(self))
        horizontalLayout.addWidget(self.createEditorPane(centralwidget))
        horizontalLayout.addWidget(self.createPreview(centralwidget))

        self.setCentralWidget(centralwidget)

        self._actEdit.changed.connect(self._previewTextEdit.setPlainText)

    def createEditorPane(self,parent):
        """
        :type parent: QWidget
        :rtype: QWidget
        """

        editorPaneLayout = QHBoxLayout()

        self._actEdit = ActEdit()

        # Create stretchable space either side of act.
        editorPaneLayout.addStretch(50)
        editorPaneLayout.addWidget(self._actEdit)
        editorPaneLayout.addStretch(50)

        editorPane = QWidget(parent)
        editorPane.setLayout(editorPaneLayout)

        return editorPane

    def createPreview(self, parent):
        """
        :type parent: QWidget
        :rtype: QWidget
        """

        self._previewTextEdit = QPlainTextEdit()

        previewBox = QGroupBox("Preview")
        previewBoxLayout = QVBoxLayout()
        previewBoxLayout.addWidget(self._previewTextEdit)
        previewBox.setLayout(previewBoxLayout)

        previewBox.setFixedWidth(300)

        return previewBox

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
        program = self._actEdit.model().translate()
        logger.info(program)
        self._previewTextEdit.setPlainText(program)
        # interpreter.interpret(program)

    def clear(self):
        self.textEdit.clear()

    def loadExample1(self):
        self.textEdit.setPlainText(self.example1)

    def loadExample2(self):
        self.textEdit.setPlainText(self.example2)

class PaletteWidget(QWidget):

    def __init__(self, parent=None):
        super(PaletteWidget, self).__init__(parent)
        self.setupUI()

    def setupUI(self):

        self.setFixedWidth(300)

        # Rather than use a lot of boiler plate code define abstract
        # structure of the palette and take care of layout later.
        # Need to use comma after element in 1-tuple for iteration.
        paletteContents = (
            (
                "Scenes",
                (
                    MiniVideoSceneWidget(),
                )
            ),
            (
                "Video and Video Collections",
                (
                    VideoValueWidget("http://www.youtube.com/watch?v=9bZkp7q19f0"),
                    VideoCollectionDefnWidget()
                )
            ),
            (
                "Numbers",
                (
                    NumberValueWidget(0),
                )
            ),
            (
                "Text",
                (
                    TextValueWidget(""),
                )
            )
        )
        paletteLayout = QVBoxLayout()

        for (label, tools) in paletteContents:
            box = QGroupBox(label)
            boxLayout = QVBoxLayout()
            for tool in tools:
                boxLayout.addWidget(tool)
            box.setLayout(boxLayout)
            paletteLayout.addWidget(box)

        paletteLayout.addStretch()
        self.setLayout(paletteLayout)
