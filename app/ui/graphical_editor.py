
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

# Externalise important strings.
_GAP_ERROR_TEXT = """Your script could not be %s because there's a gap that needs to be filled.\n
You can spot a gap that needs to be filled by it's thick border. Fill it in by dragging blocks of the same type onto it."""
_TRANSLATE_GAP_ERROR_TEXT = _GAP_ERROR_TEXT % "translated"
_PERFORM_GAP_ERROR_TEXT = _GAP_ERROR_TEXT % "performed"

class GraphicalEditor(QMainWindow):
    
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
        
        editorPane = self.createEditorPane(centralwidget)
        palette = PaletteWidget(self._scriptEdit, self)
        
        horizontalLayout.addWidget(palette)
        horizontalLayout.addWidget(editorPane)
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

        # Editor should take up as much space as possible however leave some padding for visible seperation.
        editorPaneLayout.addSpacing(10)
        editorPaneLayout.addWidget(self._scriptEdit)
        editorPaneLayout.addSpacing(10)

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

        performAction = QAction('Perform', self)
        performAction.setStatusTip('Perform script')
        performAction.setToolTip('Perform script')
        performAction.triggered.connect(self.perform)

        clearAction = QAction('Clear', self)
        clearAction.setStatusTip('Clear script')
        clearAction.setToolTip('Clear script')
        clearAction.triggered.connect(self._scriptEdit.clear)

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

        toolbar.addAction(performAction)
        toolbar.addAction(clearAction)
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
            QMessageBox.information(self, "Found a gap",
                _TRANSLATE_GAP_ERROR_TEXT, QMessageBox.Ok)

    def perform(self):
        try:
            script = self._scriptEdit.toPython()
            interpreter.interpret(script)
        except language.GapError:
            QMessageBox.information(self, "Found a gap",
                _PERFORM_GAP_ERROR_TEXT, QMessageBox.Ok)

    def loadExample1(self):
        example = language.Act([
            language.TextScene(
                "Displays the title of a video, click `perform` to find out what it it!",
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
                    language.VideoSetVariableStatement(
                        "curr_video",
                        language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
                    )
                ]),
                language.CommandSequence([]),
                language.YoutubeVideoGetTitle(language.VideoGetVariableExpression("curr_video"))
            ),
            language.VideoScene(
                "This scene plays Gangnam Style.",
                "We get hold of the video by using the variable we stored it in earlier.",
                language.NumberValue(10),
                language.CommandSequence([]),
                language.CommandSequence([]),
                language.NumberValue(0),
                language.VideoGetVariableExpression("curr_video")
            ),
            language.TextScene(
                "Display title of a related video.",
                "We select a random related video and use that from now on.",
                language.NumberValue(2),
                language.CommandSequence([
                    language.VideoSetVariableStatement(
                        "curr_video",
                        language.YoutubeVideoCollectionRandom(
                            language.YoutubeVideoGetRelated(
                                language.VideoGetVariableExpression("curr_video")
                            )
                        )
                    )
                ]),
                language.CommandSequence([]),
                language.YoutubeVideoGetTitle(language.VideoGetVariableExpression("curr_video"))
            ),
            language.VideoScene(
                "This scene plays the related video.",
                "",
                language.NumberValue(10),
                language.CommandSequence([]),
                language.CommandSequence([]),
                language.NumberValue(0),
                language.VideoGetVariableExpression("curr_video")
            )
        ])
        self._scriptEdit.setScript(example)

class ScriptEdit(QScrollArea):
    """
    Component of interface that provides an editor for the language.

    Provides similiar interface to native editor classes like QLineEdit.
    """

    # A change has been made and script is without gaps.
    changed = Signal(str)

    # Set of live variables changed.
    # List used as need to keep order within combo box consistent, for simplicity of implementation.
    liveNumberVariablesChanged = Signal(list)
    liveTextVariablesChanged = Signal(list)
    liveVideoVariablesChanged = Signal(list)
    liveVideoCollectionVariablesChanged = Signal(list)

    def __init__(self, parent=None):
        super(ScriptEdit, self).__init__(parent)
        self.setMinimumWidth(700)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
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

    @Slot(language.Act)
    def setScript(self, script):
        """
        :type script: language.Act
        """
        actWidget = LanguageWidgetFactory.build(script, self)
        self._setActWidget(actWidget)

        self.changed.emit(self.toPython())

    def toModel(self):
        """
        Provides Language Component model interface to script.

        :rtype: language.Act
        :raises: language.GapError 
        """
        return self._actWidget.model()

    def toPython(self):
        """
        Provides Python interface to script.

        :rtype: str
        :raises: language.GapError
        """
        return self.toModel().translate()

    @Slot()
    def clear(self):
        """
        Sets script to act with no scenes.
        """
        script = language.Act([])
        self.setScript(script)

    @Slot(language.LanguageComponent)
    def highlightAccepting(self, component):
        """
        Highlights all gaps in current script that could accept component.

        :type component: language.LanguageComponent
        """
        for gap in self._acceptingGaps(component):
            gap.highlight()

    @Slot()
    def unhighlightAll(self):
        """
        Unhighlights all language components in current script.
        """
        for gap in self._gaps():
            gap.unhighlight()

    def _gaps(self):
        """
        Returns all gap widgets in current script.

        :rtype: QWidget sequence
        """
        gap_widget_types = (GapWidget, ListGapWidget)
        child_lists = map(self._actWidget.findChildren, gap_widget_types)
        # Flatten lists
        return [child for child_list in child_lists for child in child_list]

    def _acceptingGaps(self, component):
        """
        Returns all gap widgets that could accept language component.

        :type component: language.LanguageComponent
        :rtype: QWidget sequence
        """
        return filter(lambda gap: gap.isAcceptable(component), self._gaps())

    def event(self, event):
        """
        Reimplement so can handle script change events.
        """
        if event.type() == events.ScriptChangeType:
            self.scriptChangeEvent(event)
            # Return true to indicate have handled event.
            # Rapid GUI Programming pg310
            return True
        # elif event.type() == events.LiveNumberVariablesChangeType:
        #     self.liveNumberVariablesChanged.emit(self.liveNumberVariables())
        #     print self.liveNumberVariables()
        #     return True
        else:
            # Use base class implementation to handle other events.
            return super(ScriptEdit, self).event(event)

    def scriptChangeEvent(self, scriptChangeEvent):
        """
        Emit changed signal if there are no gaps.

        :type scriptChangeEvent: events.ScriptChangeType
        """
        try:
            self.changed.emit(self.toPython())
        except language.GapError:
            pass

    def _liveNumberVariables(self):
        return self._actWidget.get_live_variable(language.Type.NUMBER)

    def _liveTextVariables(self):
        return self._actWidget.get_live_variable(language.Type.TEXT)

    def _liveVideoVariables(self):
        return self._actWidget.get_live_variable(language.Type.VIDEO)

    def _liveVideoCollectionVariables(self):
        return self._actWidget.get_live_variable(language.Type.VIDEO_COLLECTION)

    @Slot(list)
    def setLiveNumberVariables(names):
        self.liveNumberVariablesChanged.emit(names)

    @Slot(list)
    def setLiveTextVariables(names):
        self.liveTextVariablesChanged.emit(names)

    @Slot(list)
    def setLiveVideoVariables(names):
        self.liveVideoVariablesChanged.emit(names)

    @Slot(list)
    def setLiveVideoCollectionVariables(names):
        self.liveVideoCollectionVariablesChanged.emit(names)

class PaletteWidget(QToolBox):
    """
    Component of interface that provides a palette of language components.
    """

    def __init__(self, scriptEdit, parent=None):
        """
        :type scriptEdit: ScriptEdit
        """
        super(PaletteWidget, self).__init__(parent)
        self._scriptEdit = scriptEdit
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
                    YoutubeVideoGetRelatedWidget(language.YoutubeVideoGetRelated(language.VideoGap()), self),
                    YoutubeSearchWidget(language.YoutubeSearch(language.TextValue("music")), self),
                    YoutubeTopRatedWidget(self),
                    YoutubeMostViewedWidget(self),
                    YoutubeRecentlyFeaturedWidget(self),
                    YoutubeMostRecentWidget(self)
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
                    YoutubeVideoGetTitleWidget(language.YoutubeVideoGetTitle(language.VideoGap()), self),
                    YoutubeVideoRandomCommentWidget(language.YoutubeVideoRandomComment(language.VideoGap()), self)
                )
            ),
            (
                "Variables",
                (
                    NumberGetWidget(language.NumberGetVariableExpression("item"), self),
                    NumberSetWidget(language.NumberSetVariableStatement("item", language.NumberGap()), self),
                    TextGetWidget(language.TextGetVariableExpression("item"), self),
                    TextSetWidget(language.TextSetVariableStatement("item", language.TextGap()), self),
                    VideoGetWidget(language.VideoGetVariableExpression("item"), self),
                    VideoSetWidget(language.VideoSetVariableStatement("item", language.VideoGap()), self),
                    VideoCollectionGetWidget(language.VideoCollectionGetVariableExpression("item"), self),
                    VideoCollectionSetWidget(language.VideoCollectionSetVariableStatement("item", language.VideoCollectionGap()), self),
                )
            )
        )

        for (label, tools) in paletteContents:
            box = QWidget()
            boxLayout = QVBoxLayout()
            for tool in tools:
                tool.setReadOnly(True)
                tool.dragStarted.connect(self._scriptEdit.highlightAccepting)
                tool.dragFinished.connect(self._scriptEdit.unhighlightAll)
                boxLayout.addWidget(tool)
            boxLayout.addStretch()
            box.setLayout(boxLayout)
            self.addItem(box, label)
