from PySide.QtCore import *
from PySide.QtGui import *
import os.path
from os.path import join
import logging

from app.ui.language import *
from app.interpreter import interpreter
from app.models import language

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

        with open("res/style.css", "r") as f:
            self.setStyleSheet(f.read())
        
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

        self._scriptEdit.changed.connect(self._previewTextEdit.setPlainText)

    def createEditorPane(self,parent):
        """
        :type parent: QWidget
        :rtype: QWidget
        """

        editorPaneLayout = QHBoxLayout()

        self._scriptEdit = ScriptEdit(self)

        # Create stretchable space either side of act.
        editorPaneLayout.addStretch(50)
        editorPaneLayout.addWidget(self._scriptEdit)
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

        translateAction = QAction('Translate', self)
        translateAction.setShortcut('Ctrl+T')
        translateAction.setStatusTip('Translate Program')
        translateAction.triggered.connect(self.translate)

        runAction = QAction('Run', self)
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip('Run Program')
        runAction.triggered.connect(self.run)

        clearAction = QAction('Clear', self)
        clearAction.setShortcut('Ctrl+E')
        clearAction.setStatusTip('Clear Program')
        clearAction.triggered.connect(self.clear)

        loadExample1Action = QAction('Load Example 1', self)
        loadExample1Action.setStatusTip('Replace current script with example 1')
        loadExample1Action.triggered.connect(self.loadExample1)

        loadExample2Action = QAction('Load Example 2', self)
        loadExample2Action.setStatusTip('Replace current script with example 2')
        loadExample2Action.triggered.connect(self.loadExample2)

        toolbar = self.addToolBar('Tools')
        toolbar.addAction(translateAction)
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

    def translate(self):
        try:
            script = self._scriptEdit.toPython()
            self._previewTextEdit.setPlainText(script)
        except language.GapError:
            self._previewTextEdit.setPlainText("Could not translate - encountered Gap.")

    def run(self):
        script = self._scriptEdit.toPython()
        interpreter.interpret(script)

    def clear(self):
        raise NotImplementedError

    def loadExample1(self):
        raise NotImplementedError

    def loadExample2(self):
        raise NotImplementedError

class ScriptEdit(QScrollArea):
    """
    Component of interface that provides an editor for the language.

    Provides similiar interface to native editor classes like QLineEdit.
    """

    # A change has been made.
    changed = Signal()

    def __init__(self, parent=None):
        super(ScriptEdit, self).__init__(parent)
        self.setMinimumWidth(600)
        self.clear()

    def _setActWidget(self, actWidget):
        """
        :type actWidget: QWidget
        """
        container = QWidget()

        containerLayout = QHBoxLayout()
        containerLayout.addStretch()
        containerLayout.addWidget(actWidget)
        actWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        actWidget.setMinimumSize(QSize(500,2000))
        containerLayout.addStretch()

        container.setLayout(containerLayout)
        # horizontal, vertical
        self.setWidget(container)

    def setScript(self, script):
        """
        :type script: language.Act
        """
        actWidget = LanguageWidgetFactory.build(script, self)
        self._setActWidget(actWidget)

    def toModel(self):
        """
        Provides Language Component model interface to script.

        :rtype: language.Act
        """
        return self.widget().model()

    def toPython(self):
        """
        Provides Python interface to script.

        :rtype: str
        """
        return self.toModel().translate()

    def clear(self):
        """
        Sets script to act with no scenes.
        """
        script = language.Act([])
        self.setScript(script)

class PaletteWidget(QWidget):
    """
    Component of interface that provides a palette of language components.
    """

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
                    MiniTextSceneWidget(self),
                    MiniVideoSceneWidget(self),
                )
            ),
            (
                "Video and Video Collections",
                (
                    VideoValueWidget(language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0"), self),
                    YoutubeVideoCollectionRandomWidget(language.YoutubeVideoCollectionRandom(language.VideoGap()), self),
                    YoutubeVideoGetRelatedWidget(language.YoutubeVideoGetRelated(language.VideoGap()), self)
                )
            ),
            (
                "Numbers",
                (
                    NumberValueWidget(language.NumberValue(0), self),
                    NumberOperatorWidget("+", language.NumberGap(), language.NumberGap(), self)
                )
            ),
            (
                "Text",
                (
                    TextValueWidget(language.TextValue(""), self),
                    YoutubeVideoGetTitleWidget(language.YoutubeVideoGetTitle(language.VideoGap()), self)
                )
            ),
            (
                "Variables",
                (
                    GetWidget(language.GetVariableExpression("item"), self),
                    SetWidget(language.SetVariableStatement("item", language.NumberGap()), self),
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
