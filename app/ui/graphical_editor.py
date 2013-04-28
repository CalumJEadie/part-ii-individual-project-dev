
from PySide.QtCore import *
from PySide.QtGui import *
import os.path
from os.path import join
import logging
import cPickle
import datetime

from app import config
from app.ui.language import *
from app.interpreter import interpreter
from app.models import language
from app.models import examples

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

        # Stylesheet
        with open("res/style.css", "r") as f:
            self.setStyleSheet(f.read())

        # Looks awesome on Mac!
        self.setUnifiedTitleAndToolBarOnMac(True)

        # Set up palette, script edit and preview
        self._setupCentralWidget()

        self.statusBar()



        # Actions
        self._playAction = QAction('Play script', self)
        self._playAction.setStatusTip('Play script')
        self._playAction.setToolTip('play script')
        self._playAction.triggered.connect(self._perform)

        self._clearAction = QAction('New script', self)
        self._clearAction.setStatusTip('Replace current script with an empty script')
        self._clearAction.setToolTip('Replace current script with an empty script')
        self._clearAction.triggered.connect(self._scriptEdit.clear)

        self._saveAction = QAction('Save', self)
        self._saveAction.setShortcut(QKeySequence.Save)
        self._saveAction.setStatusTip('Save script to file')
        self._saveAction.setToolTip('Save script to file')
        self._saveAction.triggered.connect(self._save)

        self._openAction = QAction('Open', self)
        self._openAction.setShortcut(QKeySequence.Open)
        self._openAction.setStatusTip('Open script from file')
        self._openAction.setToolTip('Open script from file')
        self._openAction.triggered.connect(self._open)

        self._screenshotAction = QAction('Take screenshot', self)
        self._screenshotAction.setShortcut(QKeySequence("Ctrl+T"))
        self._screenshotAction.setStatusTip('Take screenshot of desktop')
        self._screenshotAction.setToolTip('Take screenshot of desktop')
        self._screenshotAction.triggered.connect(self._screenshot)

        self._evaluateLoadPerformanceAction = QAction("Evaluate load performance", self)
        self._evaluateLoadPerformanceAction.triggered.connect(self._evaluateLoadPerformance)        

        # Lambda not working so using inner function.
        def loadExample(self, n):
            def f():
                self._loadExample(n)
            return f

        self._loadExampleActions = []
        for i in range(0,len(examples.acts)):
            act = examples.acts[i]

            action = QAction('Open example script #%s: %s' % (str(i+1), act.title), self)
            action.setStatusTip('Replace current script with example script #%s: %s' % (str(i+1), act.title))
            action.setToolTip('Replace current script with example script #%s: %s' % (str(i+1), act.title))
            action.triggered.connect(loadExample(self, i))
            self._loadExampleActions.append(action)

        self._setupMenubar()
        self._setupToolbar()

        # Do at end to size is correct.
        self._setupWindow()

        self.show()

    def _setupCentralWidget(self):
        
        # Set up layout

        centralwidget = QWidget(self)

        horizontalLayout = QHBoxLayout(centralwidget)

        # Add toolbar and editor pane
        
        editorPane = self._createEditorPane(centralwidget)
        palette = PaletteWidget(self._scriptEdit, self)
        preview = self._createPreview(centralwidget)

        splitter = QSplitter()
        splitter.addWidget(editorPane)
        splitter.addWidget(preview)
        
        horizontalLayout.addWidget(palette)
        horizontalLayout.addWidget(splitter)

        self.setCentralWidget(centralwidget)

        self._scriptEdit.changed.connect(self._previewTextEdit.setPlainText)

    def _createEditorPane(self,parent):
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

    def _createPreview(self, parent):
        """
        :type parent: QWidget
        :rtype: QWidget
        """

        self._previewTextEdit = QPlainTextEdit()
        self._previewTextEdit.setFixedWidth(config.PREVIEW_WIDTH)
        self._previewTextEdit.setReadOnly(True)

        # previewBox = QGroupBox("Preview")
        # previewBoxLayout = QVBoxLayout()
        # previewBoxLayout.addWidget(self._previewTextEdit)
        # previewBox.setLayout(previewBoxLayout)

        # previewBox.setFixedWidth(350)

        # return previewBox
        
        return self._previewTextEdit
        
    def _setupMenubar(self):

        # From docs: If you want all windows in a Mac application to share one menu bar,
        # you must create a menu bar that does not have a parent
        # http://srinikom.github.com/pyside-docs/PySide/QtGui/QMenuBar.html
        menubar = QMenuBar()

        fileMenu = menubar.addMenu('&File')

        fileMenu.addAction(self._openAction)
        fileMenu.addAction(self._saveAction)
        fileMenu.addAction(self._screenshotAction)

        fileMenu.addSeparator()

        # fileMenu.addAction(self._loadExample1Action)
        # fileMenu.addAction(self._loadExample2Action)
        for action in self._loadExampleActions:
            fileMenu.addAction(action)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self._clearAction)

        performanceMenu = menubar.addMenu('&Performance')
        performanceMenu.addAction(self._playAction)

        evaluationMenu = menubar.addMenu("Evaluation")
        evaluationMenu.addAction(self._evaluateLoadPerformanceAction)

        self.setMenuBar(menubar)

    def _setupToolbar(self):

        toolbar = self.addToolBar('Tools')
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        toolbar.addAction(self._clearAction)
        toolbar.addSeparator()
        toolbar.addAction(self._playAction)
        toolbar.addSeparator()

        loadMenu = QMenu()

        # toolbar.addAction(self._loadExample1Action)
        # toolbar.addAction(self._loadExample2Action)
        for action in self._loadExampleActions:
            # toolbar.addAction(action)
            loadMenu.addAction(action)

        loadButton = QToolButton(self)
        loadButton.setText("Open an example script")
        loadButton.setToolButtonStyle(Qt.ToolButtonTextOnly)
        loadButton.setMenu(loadMenu)
        loadButton.setPopupMode(QToolButton.InstantPopup)
        # loadButton.triggered.connect(lambda:)

        toolbar.addWidget(loadButton)

    def _setupWindow(self):

        # self.resize(1400,800)
        # self._center()
        self.setWindowTitle('%s - Graphical Editor' % config.APP_NAME)
        self.showMaximized()  
        
    def _center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _translate(self):
        try:
            script = self._scriptEdit.toPython()
            self._previewTextEdit.setPlainText(script)
        except language.GapError:
            QMessageBox.information(self, "Found a gap",
                _TRANSLATE_GAP_ERROR_TEXT, QMessageBox.Ok)

    def _perform(self):
        try:
            script = self._scriptEdit.toPython()
            interpreter.interpret(script)
        except language.GapError:
            QMessageBox.information(self, "Found a gap",
                _PERFORM_GAP_ERROR_TEXT, QMessageBox.Ok)

    def _loadExample1(self):
        self._scriptEdit.setScript(examples.acts[0])

    def _loadExample2(self):
        self._scriptEdit.setScript(examples.acts[1])

    def _loadExample(self, n):
        self._scriptEdit.setScript(examples.acts[n])

    def _save(self):
        now = datetime.datetime.now()

        filePath = "%s/%s.%s" % (config.APP_DIR, now.strftime("%Y-%m-%d-%H-%M-%S"), config.SCRIPT_EXTENSION)
        
        with open(filePath, 'w') as f:
            cPickle.dump(self._scriptEdit.toModel(), f)

        QMessageBox.information(self, "Save", "Script saved to %s" % filePath, QMessageBox.Ok)

    def _open(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open script from file',
            config.APP_DIR, "Script files (*.%s)" % config.SCRIPT_EXTENSION)
        
        with open(filePath, 'r') as f:
            self._scriptEdit.setScript(cPickle.load(f))

    def _screenshot(self):
        now = datetime.datetime.now()
        filePath = "%s/%s.%s" % (config.APP_DIR, now.strftime("%Y-%m-%d-%H-%M-%S"), config.SCREENSHOT_FORMAT)

        screenPixmap = QPixmap.grabWindow(QApplication.desktop().winId())

        screenPixmap.save(filePath, config.SCREENSHOT_FORMAT)

        QMessageBox.information(self, "Screenshot", "Screenshot saved to %s" % filePath, QMessageBox.Ok)

    def _evaluateLoadPerformance(self):
        logger.info("Starting evaluation of load performance.")

        for i in range(0,len(examples.acts)):
            act = examples.acts[i]

            logger.info("Script #: %s" % str(i+1))
            logger.info("Title: %s" % act.title)

            logger.info("Loading example...")
            self._loadExample(i)
            logger.info("Example loading...")

        logger.info("Completed evaluation of load performance.")

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
        self.setMinimumWidth(config.SCRIPT_EDIT_MIN_WIDTH)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setAlignment(Qt.AlignHCenter) # Place script in center of edit
        self.setWidgetResizable(True) # Neccessary to take advantage of available space.
        self.clear()

        self._emptyGapsAnimationTimer = QTimer()
        self._emptyGapsAnimationTimer.setInterval(config.EMPTY_GAP_ANIMATION_INTERVAL)
        self._emptyGapsAnimationTimer.timeout.connect(self._animateEmptyGaps)
        self._gapsHighlighted = False

        self._startEmptyGapsAnimation()

    def _setActWidget(self, actWidget):
        """
        :type actWidget: QWidget
        """
        self._actWidget = actWidget

        actWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.setWidget(self._actWidget)

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
        script = language.Act("", [])
        self.setScript(script)

    @Slot(language.LanguageComponent)
    def highlightAccepting(self, component):
        """
        Highlights all gaps in current script that could accept component.

        :type component: language.LanguageComponent
        """
        for gap in self._acceptingGaps(component):
            gap.increaseHighlight()

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

    def _emptyGaps(self):
        """
        Returns all gap widgets that are empty.

        Specifically subclasses of GapWidget rather than ListGapWidget.

        :rtype: GapWidget sequence
        """
        gaps = filter(lambda gap: isinstance(gap, GapWidget), self._gaps())
        return filter(lambda gap: not gap.isFull(), gaps)

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

    def _startEmptyGapsAnimation(self):
        self._emptyGapsAnimationTimer.start()

    def _animateEmptyGaps(self):
        """
        Perform animation of empty gaps.

        Gap highlight level mechanism makes sure don't interfere
        with other mechanisms.
        """
        emptyGaps = self._emptyGaps()

        if self._gapsHighlighted:
            for gap in emptyGaps:
                gap.decreaseHighlight()
        else:
            for gap in emptyGaps:
                gap.increaseHighlight()

        self._gapsHighlighted = not self._gapsHighlighted

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

        self.setFixedWidth(config.PALETTE_WIDTH)

        # Rather than use a lot of boiler plate code define abstract
        # structure of the palette and take care of layout later.
        # Need to use comma after element in 1-tuple for iteration.
        paletteContents = (
            (
                "Scenes",
                (
                    MiniTextSceneWidget(self),
                    MiniVideoSceneWidget(self),
                    MiniIfSceneWidget(self),
                    MiniWhileSceneWidget(self)
                )
            ),
            (
                "Video",
                (
                    VideoValueWidget(language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0"), self),
                    YoutubeVideoCollectionRandomWidget(language.YoutubeVideoCollectionRandom(language.VideoGap()), self),
                    MiniVideoValueWidget("Gangnam Style", examples.GANGNAM_STYLE, self),
                    MiniVideoValueWidget("Dramatic Suprise\non a quiet square", examples.SURPRISE, self),
                    MiniVideoValueWidget("Felix's freefall\nfrom 128k", examples.FREEFALL, self),
                    MiniVideoValueWidget("Kid President's\nPep Talk", examples.PEP_TALK, self),
                    MiniVideoValueWidget("World's Largest\nRope Swing", examples.ROPE_SWING, self),
                    MiniVideoValueWidget("Fireworks", examples.FIREWORKS, self),
                    MiniVideoValueWidget("Mountain Biking", examples.MAC_ASKILL, self),
                    MiniVideoValueWidget("Cambridge Harlem", examples.CAMBRIDGE_HARLEM, self),
                )
            ),
            (
                "Video Collections",
                (
                    YoutubeVideoGetRelatedWidget(language.YoutubeVideoGetRelated(language.VideoGap()), self),
                    YoutubeSearchWidget(language.YoutubeSearch(language.TextValue("keywords")), self),
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
                    NumberOperatorWidget("+", language.NumberGap(), language.NumberGap(), self),
                    GetRandomNumberBetweenIntervalWidget(language.NumberGap(), language.NumberGap(), self),
                    YoutubeVideoGetDurationWidget(language.YoutubeVideoGetDuration(language.VideoGap()), self),
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
                "Store value commands",
                (
                    NumberSetWidget(language.NumberSetVariableStatement("number 1", language.NumberGap()), self),
                    TextSetWidget(language.TextSetVariableStatement("text 1", language.TextGap()), self),
                    VideoSetWidget(language.VideoSetVariableStatement("curr video", language.VideoGap()), self),
                    VideoCollectionSetWidget(language.VideoCollectionSetVariableStatement("collection 1", language.VideoCollectionGap()), self),
                )
            ),
            (
                "Get stored values",
                (
                    NumberGetWidget(language.NumberGetVariableExpression("number 1"), self),
                    TextGetWidget(language.TextGetVariableExpression("text 1"), self),
                    VideoGetWidget(language.VideoGetVariableExpression("curr video"), self),
                    VideoCollectionGetWidget(language.VideoCollectionGetVariableExpression("collection 1"), self),
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
