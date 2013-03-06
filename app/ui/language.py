"""
Representation of language components.

Follow naming conventions used in PySide.

- Getters omit get, setters include.
- lowerCamelCase for methods and variables.
- Methods that append use "add", those that support an index use "insert".
"""


from PySide.QtGui import *
from PySide.QtCore import *
import logging
import cPickle

from app.models import language
from app.models.language import Type
from app.api import youtube
from app.api.videoplayer import Speed
from app.ui import core, events

from show import show

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# MIME format for language components.
LC_MIME_FORMAT = "application/x-language-component"

# Use static variable set for simplicity of implementation.
# Use Jorma Sajaniemi's Roles of Variables research to inform what variables to
# provide in static sets.
# http://www.cs.joensuu.fi/~saja/var_roles/role_intro.html

# Provide variables for likely uses based on motivating applications and general
# names for other use cases.
NUMBER_VARIABLE_NAMES = ["duration", "offset", "number 1", "number 2", "number 3"]
TEXT_VARIABLE_NAMES = ["title", "comment", "text 1", "text 2", "text 3"]
VIDEO_VARIABLE_NAMES = ["curr video", "video 1", "video 2", "video 3"]
# Not obvious how to make combo box display many lines so shortern from video collection -> collection.
VIDEO_COLLECTION_VARIABLE_NAMES = ["collection 1", "collection 2", "collection 3"]

# Use mappings to avoid large large switch and define here to avoid redefines in every function.
TYPE_TO_GET_VARIABLE_EXPRESSION = {
    Type.NUMBER: language.NumberGetVariableExpression,
    Type.TEXT: language.TextGetVariableExpression,
    Type.VIDEO: language.VideoGetVariableExpression,
    Type.VIDEO_COLLECTION: language.VideoCollectionGetVariableExpression
}

TYPE_TO_SET_VARIABLE_STATEMENT = {
    Type.NUMBER: language.NumberSetVariableStatement,
    Type.TEXT: language.TextSetVariableStatement,
    Type.VIDEO: language.VideoSetVariableStatement,
    Type.VIDEO_COLLECTION: language.VideoCollectionSetVariableStatement
}

TYPE_TO_VARIABLE_NAMES = {
    Type.NUMBER: NUMBER_VARIABLE_NAMES,
    Type.TEXT: TEXT_VARIABLE_NAMES,
    Type.VIDEO: VIDEO_VARIABLE_NAMES,
    Type.VIDEO_COLLECTION: VIDEO_COLLECTION_VARIABLE_NAMES   
}

class LanguageWidgetFactory(object):
    """
    Responsible for constructing language component widgets
    from models.

    For speed of implementation this class makes extensive use of the implementation
    details of the language modes.

    An alternative would have been to have a hierachy of factory classes, one for each
    language component class where each class took responsibility for the details of
    building it's language component. This would have involved instantiation of a lot
    of very small one method classes.a lot of seperate
    classes
    """

    @staticmethod
    def build(lc, parent):
        """
        Returns language component widget for given language component
        model.

        Reverse of .model() in language component widgets.

        :type model: <:LanguageComponent
        :type parent: QWidget
        :rtype: <:QWidget
        """

        builders = {
            # language.NumberGap: lambda lc, p: NumberGapWidget(None, p),
            # language.TextGap: lambda lc, p: TextGapWidget(None, p),
            # language.VideoGap: lambda lc, p: VideoGapWidget(None, p),
            language.NumberValue: lambda lc, p: NumberValueWidget(lc, p),
            language.Add: lambda lc, p: NumberOperatorWidget("+", lc.op1, lc.op2, p),
            language.Subtract: lambda lc, p: NumberOperatorWidget("-", lc.op1, lc.op2, p),
            language.Multiply: lambda lc, p: NumberOperatorWidget("*", lc.op1, lc.op2, p),
            language.GetRandomNumberBetweenInterval: lambda lc, p: GetRandomNumberBetweenIntervalWidget(lc.op1, lc.op2, p),
            language.TextValue: lambda lc, p: TextValueWidget(lc, p),
            language.VideoValue: lambda lc, p: VideoValueWidget(lc, p),
            language.NumberGetVariableExpression: lambda lc, p: NumberGetWidget(lc, p),
            language.NumberSetVariableStatement: lambda lc, p: NumberSetWidget(lc, p),
            language.TextGetVariableExpression: lambda lc, p: TextGetWidget(lc, p),
            language.TextSetVariableStatement: lambda lc, p: TextSetWidget(lc, p),
            language.VideoGetVariableExpression: lambda lc, p: VideoGetWidget(lc, p),
            language.VideoSetVariableStatement: lambda lc, p: VideoSetWidget(lc, p),
            language.VideoCollectionGetVariableExpression: lambda lc, p: VideoCollectionGetWidget(lc, p),
            language.VideoCollectionSetVariableStatement: lambda lc, p: VideoCollectionSetWidget(lc, p),
            language.CommandSequence: lambda lc, p: CommandSequenceWidget(lc, p),
            language.TextScene: lambda lc, p: TextSceneWidget(lc, p),
            language.VideoScene: lambda lc, p: VideoSceneWidget(lc, p),
            language.IfScene: lambda lc, p: IfSceneWidget(lc, p),
            language.WhileScene: lambda lc, p: WhileSceneWidget(lc, p),
            language.YoutubeVideoGetTitle: lambda lc, p: YoutubeVideoGetTitleWidget(lc, p),
            language.YoutubeVideoGetDuration: lambda lc, p: YoutubeVideoGetDurationWidget(lc, p),
            language.YoutubeVideoRandomComment: lambda lc, p: YoutubeVideoRandomCommentWidget(lc, p),
            language.YoutubeVideoGetRelated: lambda lc, p: YoutubeVideoGetRelatedWidget(lc, p),
            language.YoutubeVideoCollectionRandom: lambda lc, p: YoutubeVideoCollectionRandomWidget(lc, p),
            language.YoutubeSearch: lambda lc, p: YoutubeSearchWidget(lc, p),
            language.SceneSequence: lambda lc, p: SceneSequenceWidget(lc, p),
            language.Act: lambda lc,p: ActWidget(lc, p),
            language.YoutubeTopRated: lambda lc, p: YoutubeTopRatedWidget(p),
            language.YoutubeMostViewed: lambda lc, p: YoutubeMostViewedWidget(p),
            language.YoutubeRecentlyFeatured: lambda lc, p: YoutubeRecentlyFeaturedWidget(p),
            language.YoutubeMostRecent: lambda lc, p: YoutubeMostRecentWidget(p),
        }

        try:
            return builders[lc.__class__](lc, parent)
        except KeyError as e:
            raise RuntimeError("Attempted to build language component with no associated builder.\n%s" % e)

class DraggableMixin(object):
    """
    Provides draggable behavior to child class.

    Child class:
    - Should subclass QWidget.
    - Should provide a method model() : () -> language.LanguageComponent.
    - Should put DraggableMixin earlier in the Method Resolution Order so override
      methods of parent class.
    """

    # setDragEnabled only available on some widgets so have to implement startDrag
    # and make sure it gets called by implementing mouseMoveEvent.
    # See Rapid GUI Programing with PyQt pg 326.
    
    # Emitted whenever a drag of the widget has started.
    dragStarted = Signal(language.LanguageComponent)

    # Emitted whenever a drag of the widget has finished, whether successful or not.
    dragFinished = Signal()
    
    def startDrag(self):
        lc = self.model()

        # Notify other widgets that drag has started.
        self.dragStarted.emit(lc)

        data = cPickle.dumps(lc)
        mimeData = QMimeData()
        mimeData.setData(LC_MIME_FORMAT, data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)

        # Wait on drag
        drag.start(Qt.CopyAction)

        # Notify other widgets that drag has finished.
        self.dragFinished.emit()

    def mouseMoveEvent(self, event):
        self.startDrag()
        QWidget.mouseMoveEvent(self, event)

class DroppableMixin(object):
    """
    Provides droppable behavior to a child class.

    Child class:
    - Should subclass QWidget.
    - Should put DraggableMixin earlier in the Method Resolution Order so override
      methods of parent class.
    - Should call self.setAcceptDrops(True)
    - Should implement isAcceptable()
    - Should implement dropEvent()
    - Should have property self._readOnly
    """

    def _extractLanguageComponent(self, event):
        """
        :type event: QDragDropEvent
        :rtype: language.LanguageComponent
        """
        return cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))   

    def dragEnterEvent(self, event):
        if not self._readOnly:
            if event.mimeData().hasFormat(LC_MIME_FORMAT):
                languageComponent = self._extractLanguageComponent(event)
                if self.isAcceptable(languageComponent):
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore() 

    def isAcceptable(self, component):
        """
        Uses template design pattern.

        :type component: language.LanguageComponent
        :rtype: boolean
        :return: True, if gap accepts components of the type of `component`.
        """
        raise NotImplementedError

    def dropEvent(self, event):
        raise NotImplementedError

class ChangeableMixin(object):
    """
    Provides changeable behavior to child class.

    Child class:
    - Should subclass QWidget.
    - Should put DraggableMixin earlier in the Method Resolution Order so override
      methods of parent class.
    - Should subclass a subclass of QWidget that does not reimplement event().
    - Should call _registerChangeSignal(signal) for each source of change signals
      in it's scope. For example a widget with two line edits should call for both.
    - Should call _postScriptChangeEvent whenever at internal manipulation changes
      the language component it represents.
    """

    def _registerChangeSignal(self, signal):
        """
        Registers a source for signals that indicate a change in the
        language component represented by this widget.
        """
        signal.connect(self._postScriptChangeEvent)

    def _postScriptChangeEvent(self):
        """
        Send script change event to this widget.
        """
        QApplication.postEvent(self, events.ScriptChangeEvent())

    def event(self, event):
        """
        Override to ignore script change event.

        Neccessary to ignore so that event will be propogated up. Default
        implementation seems to silently accept user events without doing anything
        with them.
        """
        if event.type() == events.ScriptChangeType:
            event.ignore() # Don't want to process the event.
            return False # Has been recognised but not processed.
        else:
            # Assumes that child class does not inherit an implementation
            # of event() that overrides QWidget.event().
            return QWidget.event(self, event)

class DeletableMixin(object):
    """
    Provides deletable to a child class.

    Child class:
    - Should subclass QWidget.
    - Should put DeleteableMixin earlier in the Method Resolution Order so override
      methods of parent class.
    - Should have a parent with deleteScene(scene)
    """    
        
    def delete(self):
        # Use parent scene sequence widget to delete.
        self.parent().deleteScene(self)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.addAction("Delete", self.delete)
        menu.exec_(event.globalPos())

# class SignalEventMappingMixin(object):
#     """
#     Provides ability for a widget to post an event in response to recieving a signal.
#     """

#     def _event_types....
#         """Can't create state directly in mixin so """
#         if not hasattr(self, _event_types) 

#     def _registerSignalEventMapping(self, signal, event_type, event_class):
#         """
#         :type signal: QtCore.Signal
#         :type event_type: QtCore.QEvent.Type
#         :type event_class: QtCore.QEvent
#         """
#         try:
#             self._event_types
#         except NameError:
#             self._event_types = ()

#         signal.connect(lambda: QApplication.postEvent(self, event_class()))
#         self._event_types.append(event_type)

#     def event(self, event):
#         """
#         Override to ignore any registered events.

#         Neccessary to ignore so that event will be propogated up. Default
#         implementation seems to silently accept user events without doing anything
#         with them.

#         :type event: QtCore.QEvent
#         """
#         if event.type() in self._event_types:
#             event.ignore() # Don't want to process the event.
#             return False # Has been recognised but not processed.
#         else:
#             # Assumes that child class does not inherit an implementation
#             # of event() that overrides QWidget.event().
#             return QWidget.event(self, event)

class SceneSequenceWidget(DroppableMixin, ChangeableMixin, QWidget):
    """
    Basic implementation of drag and drop. Append only.

     <gap>  <-- insert after the gap
    <scene>
     <gap>
    <scene>
     <gap>  <-- self._endGap, inserts before rather than inserting after
    """

    def __init__(self, sceneSequence, parent):
        """
        :type sceneSequence: language.SceneSequence
        """

        super(SceneSequenceWidget, self).__init__(parent)

        self.setAcceptDrops(True)
        self._readOnly = False

        self._scenes = []
        self._endGap = SceneGapWidget(self)

        self._layout = QVBoxLayout()
        self._layout.addSpacing(10)
        self._layout.addWidget(self._endGap, alignment=Qt.AlignHCenter)
        for scene in sceneSequence.scenes:
            self.addScene(scene)
        self._layout.addStretch(10)

        self.setLayout(self._layout)

    def model(self):
        """
        :rtype: models.language.SceneSequence
        """
        return language.SceneSequence(map(lambda x: x.model(), self._scenes))

    def addScene(self, scene):
        """
        Appends scene to the end of the script, just before the last gap.

        :type scene: language.Scene
        """
        self.insertScene(self._endGap, scene)

    def insertScene(self, gap, scene):
        """
        Inserts scene after the gap.

        :type gap: SceneGapWidget
        :type scene: language.Scene
        """

        sceneWidget = LanguageWidgetFactory.build(scene, self)

        self._insertBeforeGap(gap, sceneWidget)
        self._scenes.append(sceneWidget)

        self._postScriptChangeEvent()

    def _insertBeforeGap(self, gap, widget):
        """
        Inserts a widget into the layout before a gap.

        Adds a gap before the widget.

        :type gap: SceneGapWidget
        :type widget: QWidget
        """
        gapBefore = SceneGapWidget(self)
        self._layout.insertWidget(self._layout.indexOf(gap), widget, alignment=Qt.AlignHCenter)
        self._layout.insertWidget(self._layout.indexOf(widget), gapBefore, alignment=Qt.AlignHCenter)
        self.updateGeometry()
 
    def isAcceptable(self, component):
        return isinstance(component, language.Scene) or \
            isinstance(component, language.IfScene) or \
            isinstance(component, language.WhileScene)

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))
        self.addScene(lc)

    def deleteScene(self, sceneWidget):
        """
        :type sceneWidget: QWidget
        """
        sceneIndex = self._layout.indexOf(sceneWidget)
        gapBefore = self._layout.itemAt(sceneIndex-1).widget()

        self._layout.removeWidget(gapBefore)
        gapBefore.setParent(None)

        self._layout.removeWidget(sceneWidget)
        sceneWidget.setParent(None)
        self._scenes.remove(sceneWidget)

        self._postScriptChangeEvent()

class ActWidget(SceneSequenceWidget):
    """
    Basic implementation of drag and drop. Append only.
    """

    def __init__(self, act, parent):
        """
        :type act: language.Act
        """
        super(ActWidget, self).__init__(language.SceneSequence(act.scenes), parent)

    def model(self):
        """
        :rtype: models.language.Act
        """
        return language.Act("", map(lambda x: x.model(), self._scenes))

class SceneWidget(DeletableMixin, QFrame):

    def __init__(self,parent):
        super(SceneWidget, self).__init__(parent)

    def title(self):
        before, sep, after = self._comment.toPlainText().partition("\n")
        return before

    def comment(self):
        before, sep, after = self._comment.toPlainText().partition("\n")
        return after

    def duration(self):
        return self._duration.model()

    def preCommands(self):
        return self._preCommands.model()

    def postCommands(self):
        # return self._postCommands.model()
        return language.CommandSequence([])

class CommentWidget(core.VerticallyGrowingPlainTextEdit):

    def __init__(self, text, parent):
        super(CommentWidget, self).__init__(text, parent)
        # self.update()

class MiniVideoSceneWidget(DraggableMixin, QLabel):

    def __init__(self, parent):
        super(MiniVideoSceneWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText("Video Scene")

    def model(self):
        """
        :rtype: models.language.VideoScene
        """
        return language.VideoScene(
            "Example Video Scene",
            "Displays Gangnam Style video for 10 seconds from offset 0 seconds.",
            language.NumberValue(10),
            language.CommandSequence([]),
            language.CommandSequence([]),
            language.NumberValue(0),
            language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
        )

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        pass

class MiniTextSceneWidget(DraggableMixin, QLabel):

    def __init__(self, parent):
        super(MiniTextSceneWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText("Text Scene")

    def model(self):
        """
        :rtype: models.language.TextScene
        """
        return language.TextScene(
            "Example Text Scene",
            "Displays title of Gangnam Style video for 2 seconds.",
            language.NumberValue(2),
            language.CommandSequence([]),
            language.CommandSequence([]),
            language.YoutubeVideoGetTitle(
                language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
            )
        )

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        pass

class MiniIfSceneWidget(DraggableMixin, QLabel):

    def __init__(self, parent):
        super(MiniIfSceneWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText("Alternative Scene")

    def model(self):
        """
        :rtype: models.language.IfScene
        """
        return language.IfScene(
            "Example Alternative Scene",
            "",
            language.TextGap(),
            language.SceneSequence([]),
            language.SceneSequence([])
        )

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        pass

class MiniWhileSceneWidget(DraggableMixin, QLabel):

    def __init__(self, parent):
        super(MiniWhileSceneWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText("Repeat Scene")

    def model(self):
        """
        :rtype: models.language.WhileScene
        """
        return language.WhileScene(
            "Example Repeat Scene",
            "",
            language.TextGap(),
            language.SceneSequence([])
        )

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        pass

class SeperatorWidget(QFrame):

    def __init__(self, parent):
        super(SeperatorWidget, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)

class VideoSceneWidget(ChangeableMixin, SceneWidget):

    def __init__(self, scene, parent):
        """
        :type scene: language.VideoScene
        """
        super(VideoSceneWidget, self).__init__(parent)


        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._comment = CommentWidget(scene.title + "\n" + scene.comment, self)
        self._comment.setMaximumHeight(50)
        self._registerChangeSignal(self._comment.textChanged)
        self._preCommands = CommandSequenceWidget(scene.pre_commands, self)
        # self._postCommands = CommandSequenceWidget(scene.post_commands, self)

        videoControls = QWidget(self)
        videoControlsLayout = QGridLayout()

        self._source = VideoGapWidget(scene.source, self)
        self._duration = NumberGapWidget(scene.duration, self)
        self._offset = NumberGapWidget(scene.offset, self)
        self._volume = NumberGapWidget(scene.volume, self)

        self._speed = QComboBox()
        self._speed.insertItem(Speed.Slow+1, "slow")
        self._speed.insertItem(Speed.Normal+1, "normal")
        self._speed.insertItem(Speed.Fast+1, "fast")
        self._speed.insertItem(Speed.VFast+1, "very fast")
        self._speed.setCurrentIndex(scene.speed.value+1)
        self._registerChangeSignal(self._speed.currentIndexChanged)

        videoControlsLayout.addWidget(QLabel("play"), 0, 0)
        videoControlsLayout.addWidget(self._source, 0, 1, 1, 2)
        videoControlsLayout.addWidget(QLabel("for"), 1, 0)
        videoControlsLayout.addWidget(self._duration, 1, 1)
        videoControlsLayout.addWidget(QLabel("seconds"), 1, 2)
        videoControlsLayout.addWidget(QLabel("from offset"), 2, 0)
        videoControlsLayout.addWidget(self._offset, 2, 1)
        videoControlsLayout.addWidget(QLabel("seconds"), 2, 2)
        videoControlsLayout.addWidget(QLabel("at volume"), 3, 0)
        videoControlsLayout.addWidget(self._volume, 3, 1)
        # dB misleading
        # videoControlsLayout.addWidget(QLabel("dB"), 3, 2)
        videoControlsLayout.addWidget(QLabel("at"), 4, 0)
        videoControlsLayout.addWidget(self._speed, 4, 1)
        videoControlsLayout.addWidget(QLabel("speed"), 4, 2)

        videoControls.setLayout(videoControlsLayout)

        layout = QVBoxLayout()
        layout.addWidget(self._comment)
        layout.addWidget(SeperatorWidget(self))
        layout.addWidget(self._preCommands)
        layout.addWidget(SeperatorWidget(self))
        layout.addWidget(videoControls)
        # layout.addWidget(self._postCommands)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.VideoScene
        """
        return language.VideoScene(
            self.title(),
            self.comment(),
            self.duration(),
            self.preCommands(),
            self.postCommands(),
            self.offset(),
            self.source(),
            self.volume(),
            self.speed()
        )

    def offset(self):
        return self._offset.model()

    def source(self):
        return self._source.model()

    def volume(self):
        return self._volume.model()

    def speed(self):
        # By construction self.speed.currentIndex() uses the same range a Speed but
        # shifted by one.
        return language.SpeedValue(self._speed.currentIndex()-1)

class TextSceneWidget(ChangeableMixin, SceneWidget):

    def __init__(self, scene, parent):
        """
        :type scene: TextScene
        """
        super(TextSceneWidget, self).__init__(parent)

        
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._comment = CommentWidget(scene.title + "\n" + scene.comment, self)
        self._comment.setMaximumHeight(50)
        self._registerChangeSignal(self._comment.textChanged)
        self._preCommands = CommandSequenceWidget(scene.pre_commands, self)
        # self._postCommands = CommandSequenceWidget(scene.post_commands, self)

        textControls = QWidget(self)
        textControlsLayout = QGridLayout()

        self._text = TextGapWidget(scene.text, self)
        self._duration = NumberGapWidget(scene.duration, self)

        textControlsLayout.addWidget(QLabel("display"), 0, 0)
        textControlsLayout.addWidget(self._text, 0, 1, 1, 2)
        textControlsLayout.addWidget(QLabel("for"), 1, 0)
        textControlsLayout.addWidget(self._duration, 1, 1)
        textControlsLayout.addWidget(QLabel("seconds"), 1, 2)

        textControls.setLayout(textControlsLayout)

        layout = QVBoxLayout()
        layout.addWidget(self._comment)
        layout.addWidget(SeperatorWidget(self))
        layout.addWidget(self._preCommands)
        layout.addWidget(SeperatorWidget(self))
        layout.addWidget(textControls)
        # layout.addWidget(self._postCommands)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.TextScene
        """
        return language.TextScene(
            self.title(),
            self.comment(),
            self.duration(),
            self.preCommands(),
            self.postCommands(),
            self.text(),
        )

    def text(self):
        return self._text.model()

class IfSceneWidget(DeletableMixin, ChangeableMixin, QFrame):

    def __init__(self, scene, parent):
        """
        :type scene: language.IfScene
        """
        super(IfSceneWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # self._comment = CommentWidget(scene.title + "\n" + scene.comment, self)
        # self._comment.setMaximumHeight(50)
        # self._registerChangeSignal(self._comment.textChanged)

        self._question = TextGapWidget(scene.question, self)
        self._true_scene_sequence = SceneSequenceWidget(scene.true_scene_sequence, self)
        self._false_scene_sequence = SceneSequenceWidget(scene.false_scene_sequence, self)

        # Use stretchs so that get center alignment.
        headLayout = QHBoxLayout()
        headLayout.addStretch()
        headLayout.addWidget(QLabel("if the answer to asking", self))
        headLayout.addWidget(self._question)
        headLayout.addWidget(QLabel("is yes, then do:", self))
        headLayout.addStretch()

        layout = QVBoxLayout()
        # layout.addWidget(self._comment)
        # PySide.QtGui.QGridLayout.addWidget(arg__1, row, column, rowSpan, columnSpan[, alignment=0])
        layout.addLayout(headLayout, alignment=Qt.AlignHCenter)
        layout.addWidget(self._true_scene_sequence, alignment=Qt.AlignHCenter)
        layout.addWidget(QLabel("otherwise, do:", self), alignment=Qt.AlignHCenter)
        layout.addWidget(self._false_scene_sequence, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def title(self):
        # before, sep, after = self._comment.toPlainText().partition("\n")
        # return before
        return "Decision Scene"

    def comment(self):
        # before, sep, after = self._comment.toPlainText().partition("\n")
        # return after
        return ""

    def question(self):
        return self._question.model()

    def true_scene_sequence(self):
        return self._true_scene_sequence.model()

    def false_scene_sequence(self):
        return self._false_scene_sequence.model()

    def model(self):
        """
        :rtype: models.language.IfScene
        """
        return language.IfScene(
            self.title(),
            self.comment(),
            self.question(),
            self.true_scene_sequence(),
            self.false_scene_sequence()
        )

class WhileSceneWidget(DeletableMixin, ChangeableMixin, QFrame):

    def __init__(self, scene, parent):
        """
        :type scene: language.WhileScene
        """
        super(WhileSceneWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # self._comment = CommentWidget(scene.title + "\n" + scene.comment, self)
        # self._comment.setMaximumHeight(50)
        # self._registerChangeSignal(self._comment.textChanged)

        self._question = TextGapWidget(scene.question, self)
        self._scene_sequence = SceneSequenceWidget(scene.scene_sequence, self)

        # Use stretchs so that get center alignment.
        headLayout = QHBoxLayout()
        headLayout.addStretch()
        headLayout.addWidget(QLabel("while the answer to asking", self))
        headLayout.addWidget(self._question)
        headLayout.addWidget(QLabel("is yes, repeatedly do:", self))
        headLayout.addStretch()

        layout = QVBoxLayout()
        # layout.addWidget(self._comment)
        # PySide.QtGui.QGridLayout.addWidget(arg__1, row, column, rowSpan, columnSpan[, alignment=0])
        layout.addLayout(headLayout, alignment=Qt.AlignHCenter)
        layout.addWidget(self._scene_sequence, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def title(self):
        # before, sep, after = self._comment.toPlainText().partition("\n")
        # return before
        return "Repeat Scene"

    def comment(self):
        # before, sep, after = self._comment.toPlainText().partition("\n")
        # return after
        return ""

    def question(self):
        return self._question.model()

    def scene_sequence(self):
        return self._scene_sequence.model()

    def model(self):
        """
        :rtype: models.language.WhileScene
        """
        return language.WhileScene(
            self.title(),
            self.comment(),
            self.question(),
            self.scene_sequence()
        )

class CommandSequenceWidget(ChangeableMixin, QWidget):
    """
    Basic implementation of drag and drop. Append only.
    """

    def __init__(self, commands, parent):
        """
        :type commands: language.CommandSequence
        """

        super(CommandSequenceWidget, self).__init__(parent)

        self._commands = []
        self._gap = CommandGapWidget(self)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._gap, alignment=Qt.AlignHCenter)
        for command in commands:
            self.addCommand(command)
        self.setLayout(self._layout)

    def model(self):
        """
        :rtype: models.language.CommandSequence
        """
        return language.CommandSequence(map(lambda w: w.model(), self._commands))

    def addCommand(self, command):
        """
        :type command: language.Statement
        """
        commandWidget = LanguageWidgetFactory.build(command, self)
        self._addAtEnd(commandWidget)
        self._commands.append(commandWidget)

        self._postScriptChangeEvent()

    def _addAtEnd(self, widget):
        """
        Adds widget to end of layout but before gap.

        :type widget: QWidget
        """
        self._layout.insertWidget(self._layout.indexOf(self._gap), widget, alignment=Qt.AlignHCenter)

class GetWidget(ChangeableMixin, DraggableMixin, QFrame):

    def __init__(self, getExpression, parent):
        """
        :type getExpression: language.GetVariableExpression
        """
        super(GetWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._type = getExpression.type
        self._name = QComboBox(self)
        ## Allow user to add and edit names
        #self._name.setEditable(True)
        for name in TYPE_TO_VARIABLE_NAMES[self._type]:
            self._name.addItem(name)
        self._name.setCurrentIndex(self._name.findText(getExpression.name))
        self._registerChangeSignal(self._name.currentIndexChanged)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("get"))
        layout.addWidget(self._name)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.GetExpression
        """
        return TYPE_TO_GET_VARIABLE_EXPRESSION[self._type](self._name.currentText())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        ## Can't simply stop user from changing selected item but can disable editing.
        #self._name.setEditable(not ro)
        pass

class NumberGetWidget(GetWidget):

    def __init__(self, getExpression, parent):
        assert getExpression.type == Type.NUMBER
        super(NumberGetWidget, self).__init__(getExpression, parent)

class TextGetWidget(GetWidget):

    def __init__(self, getExpression, parent):
        assert getExpression.type == Type.TEXT
        super(TextGetWidget, self).__init__(getExpression, parent)

class VideoGetWidget(GetWidget):

    def __init__(self, getExpression, parent):
        assert getExpression.type == Type.VIDEO
        super(VideoGetWidget, self).__init__(getExpression, parent)

class VideoCollectionGetWidget(GetWidget):

    def __init__(self, getExpression, parent):
        assert getExpression.type == Type.VIDEO_COLLECTION
        super(VideoCollectionGetWidget, self).__init__(getExpression, parent)

class SetWidget(ChangeableMixin, DraggableMixin, QFrame):

    def __init__(self, setStatement, parent):
        """
        :type setStatement: language.TypedSetVariableStatement
        """
        super(SetWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._type = setStatement.type

        self._name = QComboBox()
        ## Allow user to add and edit names
        #self._name.setEditable(True)
        for name in TYPE_TO_VARIABLE_NAMES[self._type]:
            self._name.addItem(name)
        self._name.setCurrentIndex(self._name.findText(setStatement.name))
        self._registerChangeSignal(self._name.currentIndexChanged)

        if self._type == Type.NUMBER:
            self._value = NumberGapWidget(setStatement.value, self)
        elif self._type == Type.TEXT:
            self._value = TextGapWidget(setStatement.value, self)
        elif self._type == Type.VIDEO:
            self._value = VideoGapWidget(setStatement.value, self)
        elif self._type == Type.VIDEO_COLLECTION:
            self._value = VideoCollectionGapWidget(setStatement.value, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("set"))
        layout.addWidget(self._name)
        layout.addWidget(QLabel("to"))
        layout.addWidget(self._value)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.TypedSetVariableStatement
        """
        return TYPE_TO_SET_VARIABLE_STATEMENT[self._type](self._name.currentText(), self._value.model())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        ## Can't simply stop user from changing selected item but can disable editing.
        #self._name.setEditable(not ro)
        self._value.setReadOnly(ro)

class NumberSetWidget(SetWidget):

    def __init__(self, setExpression, parent):
        assert setExpression.type == Type.NUMBER
        super(NumberSetWidget, self).__init__(setExpression, parent)

class TextSetWidget(SetWidget):

    def __init__(self, setExpression, parent):
        assert setExpression.type == Type.TEXT
        super(TextSetWidget, self).__init__(setExpression, parent)

class VideoSetWidget(SetWidget):

    def __init__(self, setExpression, parent):
        assert setExpression.type == Type.VIDEO
        super(VideoSetWidget, self).__init__(setExpression, parent)

class VideoCollectionSetWidget(SetWidget):

    def __init__(self, setExpression, parent):
        assert setExpression.type == Type.VIDEO_COLLECTION
        super(VideoCollectionSetWidget, self).__init__(setExpression, parent)

class TextValueWidget(ChangeableMixin, DraggableMixin, QFrame):

    def __init__(self, text, parent):
        """
        :type text: language.TextValue
        """
        super(TextValueWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._text = core.HGrowingLineEdit(text.value, self)       
        self._registerChangeSignal(self._text.textChanged)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("\"", self))
        layout.addWidget(self._text)
        layout.addWidget(QLabel("\"", self))
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.TextValue
        """
        return language.TextValue(self._text.text())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._text.setReadOnly(ro)

class NumberValueWidget(ChangeableMixin, DraggableMixin, QFrame):

    def __init__(self, number, parent):
        """
        :type number: language.NumberValue
        """
        super(NumberValueWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._number = core.HGrowingLineEdit(number.value, self)
        self._number.setValidator(QDoubleValidator())
        self._registerChangeSignal(self._number.textChanged)

        layout = QHBoxLayout()
        layout.addWidget(self._number)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.NumberValue
        """
        return language.NumberValue(float(self._number.text()))

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._number.setReadOnly(ro)

class VideoValueWidget(ChangeableMixin, DraggableMixin, QFrame):

    def __init__(self, video, parent):
        """
        :type video: language.VideoValue
        """
        super(VideoValueWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self._value = core.HGrowingLineEdit(video.value, self)
        self._registerChangeSignal(self._value.textChanged)
        # TODO: Add validator
        # video_id_re = QRegExp(youtube.VIDEO_ID_RE)
        # self._value.setValidator(QRegExpValidator(video_id_re, self))
        
        layout = QHBoxLayout()

        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-64-64.png"))
        layout.addWidget(icon)

        layout.addWidget(self._value)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.VideoValue
        """
        return language.VideoValue(self._value.text())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._value.setReadOnly(ro)

class MiniVideoValueWidget(DraggableMixin, QFrame):

    def __init__(self, label, value, parent):
        """
        :type label: string
        :type value: string
        """
        super(MiniVideoValueWidget, self).__init__(parent)

        self._value = value

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                
        layout = QHBoxLayout()

        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-64-64.png"))
        layout.addWidget(icon)
        layout.addWidget(QLabel(label))

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.VideoValue
        """
        return language.VideoValue(self._value)

    def setReadOnly(self, ro):
        pass

class GapWidget(ChangeableMixin, QStackedWidget):
    """
    Provides a gap that language components can be dragged into and represented
    within.

    Currently does not support type checking or dragging out of gap.
    """

    def __init__(self, child, parent):
        """
        :param child: Child language component widget or None for no child.
        :type child: QWidget
        """

        super(GapWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.setMinimumSize(QSize(10,10))
        self._child = None

        self._readOnly = False

        # Similiar to a semaphore.
        # 0 - no highlight
        # >0 - highlight
        self._highlightLevel = 0

        self.fillGap(child)

    def model(self):
        """
        :rtype: models.language.LanguageComponent
        """
        raise NotImplementedError

    def extractLanguageComponent(self, event):
        """
        :type event: QDragDropEvent
        :rtype: language.LanguageComponent
        """
        return cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))

    def dragEnterEvent(self, event):
        if not self._readOnly:
            if event.mimeData().hasFormat(LC_MIME_FORMAT):
                languageComponent = self.extractLanguageComponent(event)
                if self.isAcceptable(languageComponent):
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.fillGap(self.extractLanguageComponent(event))

    def _emptyGap(self):
        """
        Remove widget from layout and delete.
        """
        # Remove from layout.
        # Ownership revert to application.
        self.removeWidget(self._child)
        # Delete that widgets making up the language subtree that had filled the gap.
        self._child.setParent(None)
        # Remove reference from GapWidget to the old child.
        self._child = None

    def emptyGap(self):
        """
        Removes language compoment currently in gap.

        :raises RuntimeError: If gap is not currently occupied.
        """
        if not self.isFull():
            raise RuntimeError("Gap is currently not occupied.")

        self._emptyGap()

        self._postScriptChangeEvent()

    def fillGap(self, child):
        """
        Fills gap with language component, replacing language component
        currently occupying it.

        If component is a gap the gap will be emptied and left empty.

        :type child: language.LanguageComponent
        """
        if self.isFull():
            self._emptyGap()

        # Possible that language component might be a gap, in which case correct
        # behavior is to keep empty.
        if not isinstance(child, language.Gap):
            # Not a gap
            self._child = LanguageWidgetFactory.build(child, self)
            self.insertWidget(1, self._child)
            self.setCurrentIndex(1)
        else:
            # Gap
            pass

        self._postScriptChangeEvent()

    def isFull(self):
        """
        :return: True if gap is currently occupied.
        :rtype: boolean
        """
        return self._child is not None

    def isAcceptable(self, component):
        """
        Uses template design pattern.

        :type component: language.LanguageComponent
        :rtype: boolean
        :return: True, if gap accepts components of the type of `component`.
        """
        raise NotImplementedError

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._readOnly = ro

    def increaseHighlight(self):
        """
        Use highlight levels so that many mechanisms can alter
        highlighting at the same time.

        0 - no highlight
        >0 - highlight
        """
        self._highlightLevel += 1
        if self._highlightLevel > 0:
            self.setStyleSheet("background: orange")

    def decreaseHighlight(self):
        """
        Use highlight levels so that many mechanisms can alter
        highlighting at the same time.

        0 - no highlight
        >0 - highlight
        """
        self._highlightLevel = max(0, self._highlightLevel-1)
        if self._highlightLevel == 0:
            self.setStyleSheet("")

    def unhighlight(self):
        """
        Use highlight levels so that many mechanisms can alter
        highlighting at the same time.

        0 - no highlight
        >0 - highlight
        """
        self._highlightLevel = 0
        self.setStyleSheet("")

class NumberGapWidget(GapWidget):

    def __init__(self, child, parent):
        """
        :type child: language.NumberExpression
        """
        super(NumberGapWidget, self).__init__(child, parent)
        label = QLabel("number", self)
        self.addWidget(label)

    def model(self):
        """
        :rtype: models.language.NumberExpression
        """
        if self.isFull():
            return self._child.model()
        else:
            return language.NumberGap()

    def isAcceptable(self, component):
        return isinstance(component, language.NumberExpression) or \
            isinstance(component, language.NumberGetVariableExpression)

class TextGapWidget(GapWidget):

    def __init__(self, child, parent):
        """
        :type child: language.TextExpression
        """
        super(TextGapWidget, self).__init__(child, parent)
        label = QLabel("text", self)
        self.addWidget(label)

    def model(self):
        """
        :rtype: models.language.TextExpression
        """
        if self.isFull():
            return self._child.model()
        else:
            return language.TextGap()

    def isAcceptable(self, component):
        return isinstance(component, language.TextExpression) or \
            isinstance(component, language.TextGetVariableExpression)

class VideoGapWidget(GapWidget):

    def __init__(self, child, parent):
        """
        :type child: language.VideoExpression
        """
        super(VideoGapWidget, self).__init__(child, parent)
        label = QLabel(self)
        label.setPixmap(QPixmap("res/video-64-64.png"))
        self.addWidget(label)

    def model(self):
        """
        :rtype: models.language.VideoExpression
        """
        if self.isFull():
            return self._child.model()
        else:
            return language.VideoGap()

    def isAcceptable(self, component):
        return isinstance(component, language.VideoExpression) or \
            isinstance(component, language.VideoGetVariableExpression)

class VideoCollectionGapWidget(GapWidget):

    def __init__(self, child, parent):
        """
        :type child: language.VideoCollectionExpression
        """

        super(VideoCollectionGapWidget, self).__init__(child, parent)
        label = QLabel(self)
        label.setPixmap(QPixmap("res/video-collection-64-64.png"))
        self.addWidget(label)

    def model(self):
        """
        :rtype: models.language.VideoCollectionExpression
        """
        if self.isFull():
            return self._child.model()
        else:
            return language.VideoGap()

    def isAcceptable(self, component):
        return isinstance(component, language.VideoCollectionExpression) or \
            isinstance(component, language.VideoCollectionGetVariableExpression)

class ListGapWidget(QLabel):
    """
    Provides a gap that language components can dragged onto and added to
    an associated parent.

    The general contract is that parent class must implement a method for adding
    language components to the list:
    - add: language.Command -> ()
    """

    def __init__(self, text, parent):
        """
        :type text: string
        :param parent: Used to call back for modifying items.
        """
        super(ListGapWidget, self).__init__(text, parent)
        self.setAcceptDrops(True)
        # Preferred - The sizeHint() is best, but the widget can be shrunk and still be useful.
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignHCenter)

        self._readOnly = False

    def extractLanguageComponent(self, event):
        """
        :type event: QDragDropEvent
        :rtype: language.LanguageComponent
        """
        return cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))

    def dragEnterEvent(self, event):
        if not self._readOnly:
            if event.mimeData().hasFormat(LC_MIME_FORMAT):
                languageComponent = self.extractLanguageComponent(event)
                if self.isAcceptable(languageComponent):
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def isAcceptable(self, component):
        """
        Uses template design pattern.

        :type component: language.LanguageComponent
        :rtype: boolean
        :return: True, if gap accepts components of the type of `component`.
        """
        raise NotImplementedError

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._readOnly = ro

    def increaseHighlight(self):
        self.setStyleSheet("background: orange")

    def decreaseHighlight(self):
        raise NotImplementedError

    def unhighlight(self):
        self.setStyleSheet("")

class CommandGapWidget(ListGapWidget):

    def __init__(self, parent):
        """
        :param parent: Used to call back to for modifying commands.
        :type parent: CommandSequenceWidget
        """
        super(CommandGapWidget, self).__init__("drag store value command here", parent)
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumWidth(350)
        self.setMargin(5)

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))
        self.parent().addCommand(lc)

    def isAcceptable(self, component):
        return isinstance(component, language.Statement)

class SceneGapWidget(ListGapWidget):

    def __init__(self, parent):
        """
        :param parent: Used to call back to for modifying commands.
        :type parent: ActWidget
        """
        super(SceneGapWidget, self).__init__("drag scene here", parent)
        self.setMinimumHeight(40)
        self.setMinimumWidth(300)

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))
        self.parent().insertScene(self, lc)

    def isAcceptable(self, component):
        return isinstance(component, language.Scene) or \
            isinstance(component, language.IfScene) or \
            isinstance(component, language.WhileScene)

class NumberOperatorWidget(ChangeableMixin, DraggableMixin, QFrame):

    OPERATORS = {
        "+": language.Add,
        "-": language.Subtract,
        "*": language.Multiply
    }

    def __init__(self, operator, operand1, operand2, parent):
        """
        :type operator: string
        :type operand1: language.NumberExpression
        :type operand2: language.NumberExpression
        """

        assert operator in self.OPERATORS.keys()
        super(NumberOperatorWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._operand1 = NumberGapWidget(operand1, self)
        self._operand2 = NumberGapWidget(operand2, self)

        self._operator = QComboBox()
        self._operator.addItem("+")
        self._operator.addItem("-")
        self._operator.addItem("*")
        self._operator.setCurrentIndex(self._operator.findText(operator))
        self._registerChangeSignal(self._operator.currentIndexChanged)

        layout = QHBoxLayout()
        layout.addWidget(self._operand1)
        layout.addWidget(self._operator)
        layout.addWidget(self._operand2)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.NumberValue
        """
        operator = self._operator.currentText()
        return self.OPERATORS[operator](
            self._operand1.model(),
            self._operand2.model()
        )

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        # Can't set combo box read only.
        self._operand1.setReadOnly(ro)
        self._operand2.setReadOnly(ro)



class GetRandomNumberBetweenIntervalWidget(DraggableMixin, QFrame):

    def __init__(self, operand1, operand2, parent):
        """
        :type operand1: language.NumberExpression
        :type operand2: language.NumberExpression
        """
        super(GetRandomNumberBetweenIntervalWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._operand1 = NumberGapWidget(operand1, self)
        self._operand2 = NumberGapWidget(operand2, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("random\nfrom", self))
        layout.addWidget(self._operand1)
        layout.addWidget(QLabel("to", self))
        layout.addWidget(self._operand2)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.GetRandomNumberBetweenInterval
        """
        return language.GetRandomNumberBetweenInterval(
            self._operand1.model(),
            self._operand2.model()
        )

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._operand1.setReadOnly(ro)
        self._operand2.setReadOnly(ro)

class YoutubeVideoGetTitleWidget(DraggableMixin, QFrame):

    def __init__(self, videoGetTitle, parent):
        """
        :type videoGetTitle: language.YoutubeVideoGetTitle
        """

        super(YoutubeVideoGetTitleWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._video = VideoGapWidget(videoGetTitle.video, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("title\nof", self))
        layout.addWidget(self._video)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoGetTitle
        """
        return language.YoutubeVideoGetTitle(self._video.model())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._video.setReadOnly(ro)

class YoutubeVideoGetDurationWidget(DraggableMixin, QFrame):

    def __init__(self, videoGetDuration, parent):
        """
        :type videoGetDuration: language.YoutubeVideoGetDuration
        """

        super(YoutubeVideoGetDurationWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._video = VideoGapWidget(videoGetDuration.video, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("duration\nof", self))
        layout.addWidget(self._video)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoGetDuration
        """
        return language.YoutubeVideoGetDuration(self._video.model())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._video.setReadOnly(ro)

class YoutubeVideoRandomCommentWidget(DraggableMixin, QFrame):

    def __init__(self, videoRandomComment, parent):
        """
        :type videoRandomComment: language.YoutubeVideoRandomComment
        """

        super(YoutubeVideoRandomCommentWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._video = VideoGapWidget(videoRandomComment.video, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("random\ncomment\nfrom", self))
        layout.addWidget(self._video)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoRandomComment
        """
        return language.YoutubeVideoRandomComment(self._video.model())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._video.setReadOnly(ro)

class YoutubeVideoGetRelatedWidget(DraggableMixin, QFrame):

    def __init__(self, videoGetRelated, parent):
        """
        :type videoGetRelated: language.YoutubeVideoGetRelated
        """

        super(YoutubeVideoGetRelatedWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._video = VideoGapWidget(videoGetRelated.video, self)

        layout = QHBoxLayout()
        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-collection-64-64.png"))
        layout.addWidget(icon)
        layout.addWidget(QLabel("related\nto", self))
        layout.addWidget(self._video)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoGetRelated
        """
        return language.YoutubeVideoGetRelated(self._video.model())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._video.setReadOnly(ro)

class YoutubeVideoCollectionRandomWidget(DraggableMixin, QFrame):

    def __init__(self, videoCollectionRandom, parent):
        """
        :type videoCollectionRandom: language.YoutubeVideoCollectionRandom
        """

        super(YoutubeVideoCollectionRandomWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._videoCollection = VideoCollectionGapWidget(videoCollectionRandom.video_collection, self)

        layout = QHBoxLayout()
        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-64-64.png"))
        layout.addWidget(icon)
        layout.addWidget(QLabel("random\nfrom", self))
        layout.addWidget(self._videoCollection)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoCollectionRandom
        """
        return language.YoutubeVideoCollectionRandom(self._videoCollection.model())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._videoCollection.setReadOnly(ro)

class YoutubeSearchWidget(DraggableMixin, QFrame):

    def __init__(self, youtubeSearch, parent):
        """
        :type youtubeSearch: language.YoutubeSearch
        """

        super(YoutubeSearchWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._query = TextGapWidget(youtubeSearch.query, self)

        layout = QHBoxLayout()
        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-collection-64-64.png"))
        layout.addWidget(icon)
        layout.addWidget(QLabel("search", self))
        layout.addWidget(self._query)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeSearch
        """
        return language.YoutubeSearch(self._query.model())

    def setReadOnly(self, ro):
        """
        :type ro: boolean
        """
        self._query.setReadOnly(ro)



class VideoCollectionFunction0Widget(DraggableMixin, QFrame):

    def __init__(self, lcClass, label, parent):
        """
        :type lcClass: LanguageComponent class
        :type label: string
        :type parent: QWidget
        """
        super(VideoCollectionFunction0Widget, self).__init__(parent)

        self.model = lambda: lcClass()

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout = QHBoxLayout()
        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-collection-64-64.png"))
        layout.addWidget(icon)
        layout.addWidget(QLabel(label, self))

        self.setLayout(layout)

    def setReadOnly(self, ro):
        pass

class YoutubeTopRatedWidget(VideoCollectionFunction0Widget):

    def __init__(self, parent):
        super(YoutubeTopRatedWidget, self).__init__(language.YoutubeTopRated, "top\nrated", parent)

class YoutubeMostViewedWidget(VideoCollectionFunction0Widget):

    def __init__(self, parent):
        super(YoutubeMostViewedWidget, self).__init__(language.YoutubeMostViewed, "most\nviewed", parent)

class YoutubeRecentlyFeaturedWidget(VideoCollectionFunction0Widget):

    def __init__(self, parent):
        super(YoutubeRecentlyFeaturedWidget, self).__init__(language.YoutubeRecentlyFeatured, "recently\nfeatured", parent)

class YoutubeMostRecentWidget(VideoCollectionFunction0Widget):

    def __init__(self, parent):
        super(YoutubeMostRecentWidget, self).__init__(language.YoutubeMostRecent, "most\nrecent", parent)