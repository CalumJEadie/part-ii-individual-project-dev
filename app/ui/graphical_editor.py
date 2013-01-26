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
        self.setupCentralWidget()
        self.statusBar()

        self.setupToolbar()

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
        self._previewTextEdit.setFixedWidth(350)
        self._previewTextEdit.setReadOnly(True)

        # previewBox = QGroupBox("Preview")
        # previewBoxLayout = QVBoxLayout()
        # previewBoxLayout.addWidget(self._previewTextEdit)
        # previewBox.setLayout(previewBoxLayout)

        # previewBox.setFixedWidth(350)

        # return previewBox
        
        return self._previewTextEdit
        

    def setupToolbar(self):

        runAction = QAction('Perform', self)
        runAction.setStatusTip('Perform script')
        runAction.setToolTip('Perform script')
        runAction.triggered.connect(self.run)

        clearAction = QAction('Clear', self)
        clearAction.setStatusTip('Clear script')
        clearAction.setToolTip('Clear script')
        clearAction.triggered.connect(self._scriptEdit.clear)

        translateAction = QAction('Translate', self)
        translateAction.setStatusTip('Translate script into Python code')
        translateAction.setToolTip('Translate script into Python code')
        translateAction.triggered.connect(self.translate)

        loadExample1Action = QAction('Load example script 1', self)
        loadExample1Action.setStatusTip('Replace current script with example script 1')
        loadExample1Action.setToolTip('Replace current script with example script 1')
        loadExample1Action.triggered.connect(self.loadExample1)

        loadExample2Action = QAction('Load example script 2', self)
        loadExample2Action.setStatusTip('Replace current script with example script 2')
        loadExample1Action.setToolTip('Replace current script with example script 2')
        loadExample2Action.triggered.connect(self.loadExample2)

        toolbar = self.addToolBar('Tools')
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        toolbar.addAction(runAction)
        toolbar.addAction(clearAction)
        toolbar.addAction(translateAction)
        toolbar.addSeparator()
        toolbar.addAction(loadExample1Action)
        toolbar.addAction(loadExample2Action)

    def setupWindow(self):

        # self.resize(1400,800)
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

    def loadExample1(self):
        example = language.Act([
            language.TextScene(
                "Displays the title of a video, click `run` to find out what it it!",
                "",
                language.NumberValue(2),
                language.CommandSequence([]),
                language.CommandSequence([]),
                language.YoutubeVideoGetTitle(language.VideoValue("http://www.youtube.com/watch?v=uweWiCLT8Eg")) # David Guetta - She Wolf (Lyrics Video) ft. Sia
            ),
            language.VideoScene(
                "Plays the video.",
                "",
                language.NumberValue(2),
                language.CommandSequence([]),
                language.CommandSequence([]),
                language.NumberValue(0),
                language.VideoValue("http://www.youtube.com/watch?v=uweWiCLT8Eg") # David Guetta - She Wolf (Lyrics Video) ft. Sia
            )
        ])
        self._scriptEdit.setScript(example)

    def loadExample2(self):
        example = language.Act([
            language.TextScene(
                "Use this space to write about a scene, this one displays the title of Gangnam Style.",
                "The Gangnam Style video is identified by it's web page and saved for later in the variable `curr_video`.",
                language.NumberValue(2),
                language.CommandSequence([
                    language.SetVariableStatement(
                        "curr_video",
                        language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
                    )
                ]),
                language.CommandSequence([]),
                language.YoutubeVideoGetTitle(language.GetVariableExpression("curr_video"))
            ),
            language.VideoScene(
                "This scene plays Gangnam Style.",
                "We get hold of the video by using the variable we stored it in earlier.",
                language.NumberValue(10),
                language.CommandSequence([]),
                language.CommandSequence([]),
                language.NumberValue(0),
                language.GetVariableExpression("curr_video")
            ),
            language.TextScene(
                "Display title of a related video.",
                "We select a random related video and use that from now on.",
                language.NumberValue(2),
                language.CommandSequence([
                    language.SetVariableStatement(
                        "curr_video",
                        language.YoutubeVideoCollectionRandom(
                            language.YoutubeVideoGetRelated(
                                language.GetVariableExpression("curr_video")
                            )
                        )
                    )
                ]),
                language.CommandSequence([]),
                language.YoutubeVideoGetTitle(language.GetVariableExpression("curr_video"))
            ),
            language.VideoScene(
                "This scene plays the related video.",
                "",
                language.NumberValue(10),
                language.CommandSequence([]),
                language.CommandSequence([]),
                language.NumberValue(0),
                language.GetVariableExpression("curr_video")
            )
        ])
        self._scriptEdit.setScript(example)

class ScriptEdit(QScrollArea):
    """
    Component of interface that provides an editor for the language.

    Provides similiar interface to native editor classes like QLineEdit.
    """

    # A change has been made.
    changed = Signal()

    def __init__(self, parent=None):
        super(ScriptEdit, self).__init__(parent)
        self.setMinimumWidth(700)
        self.clear()

    def _setActWidget(self, actWidget):
        """
        :type actWidget: QWidget
        """
        self._actWidget = actWidget

        container = QWidget()

        containerLayout = QHBoxLayout()
        containerLayout.addStretch()
        containerLayout.addWidget(actWidget)
        actWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        actWidget.setMinimumSize(QSize(650,2000))
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
        return self._actWidget.model()

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

class PaletteWidget(QToolBox):
    """
    Component of interface that provides a palette of language components.
    """

    def __init__(self, parent=None):
        super(PaletteWidget, self).__init__(parent)
        self.setupUI()

    def setupUI(self):

        self.setFixedWidth(350)

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

        for (label, tools) in paletteContents:
            box = QWidget()
            boxLayout = QVBoxLayout()
            for tool in tools:
                tool.setReadOnly(True)
                boxLayout.addWidget(tool)
            boxLayout.addStretch()
            box.setLayout(boxLayout)
            self.addItem(box, label)