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
from app.api import youtube
from app.ui import core

from show import show

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# MIME format for language components.
LC_MIME_FORMAT = "application/x-language-component"

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
            language.TextValue: lambda lc, p: TextValueWidget(lc, p),
            language.VideoValue: lambda lc, p: VideoValueWidget(lc, p),
            language.GetVariableExpression: lambda lc, p: GetWidget(lc, p),
            language.SetVariableStatement: lambda lc, p: SetWidget(lc, p),
            language.CommandSequence: lambda lc, p: CommandSequenceWidget(lc, p),
            language.TextScene: lambda lc, p: TextSceneWidget(lc, p),
            language.VideoScene: lambda lc, p: VideoSceneWidget(lc, p),
            language.YoutubeVideoGetTitle: lambda lc, p: YoutubeVideoGetTitleWidget(lc, p),
            language.YoutubeVideoGetRelated: lambda lc, p: YoutubeVideoGetRelatedWidget(lc, p),
            language.YoutubeVideoCollectionRandom: lambda lc, p: YoutubeVideoCollectionRandomWidget(lc, p),
            language.Act: lambda lc,p: ActWidget(lc, p)
        }

        try:
            return builders[lc.__class__](lc, parent)
        except KeyError as e:
            raise RuntimeError("Attempted to build language component with no associated builder.\n%s" % e)


class ActWidget(QWidget):
    """
    Basic implementation of drag and drop. Append only.
    """

    def __init__(self, act, parent):
        """
        :type act: language.Act
        """

        super(ActWidget, self).__init__(parent)

        self._scenes = []
        self._gap = SceneGapWidget(self)

        self._layout = QVBoxLayout()
        self._layout.addSpacing(10)
        self._layout.addWidget(self._gap)
        for scene in act.scenes:
            self.addScene(scene)
        self._layout.addStretch(10)

        self.setLayout(self._layout)

    # def _setupUI(self):
    #     layout = QVBoxLayout()
    #     layout.addSpacing(10)
    #     for scene in self._scenes:
    #         layout.addWidget(scene)
    #     layout.addStretch(10)
        # self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.Act
        """
        return language.Act(map(lambda x: x.model(), self._scenes))

    # def mousePressEvent(self,event):
    #     self.changed.emit(self.model().translate())

    def addScene(self, scene):
        """
        :type scene: language.Scene
        """
        sceneWidget = LanguageWidgetFactory.build(scene, self)
        self._addAtEnd(sceneWidget)
        self._scenes.append(sceneWidget)

    def _addAtEnd(self, widget):
        """
        Adds widget to end of layout but before gap.

        :type widget: QWidget
        """
        self._layout.insertWidget(self._layout.indexOf(self._gap), widget)

class SceneWidget(QFrame):

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
        return self._postCommands.model()

class CommentWidget(core.VerticallyGrowingPlainTextEdit):

    def __init__(self, text, parent):
        super(CommentWidget, self).__init__(text, parent)
        # self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Qt.ScrollBarAsNeeded
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # fm = QFontMetrics(self.font())
        # h = fm.height() * 1.6
        # self.setMinimumHeight(h)

        # self.setMaximumHeight(50)

class DraggableMixin(object):
    """
    Provides draggable behavior to child class.

    Child class:
    - Must subclass QWidget.
    - Must provide a method model() : () -> language.LanguageComponent.
    - Must put DraggableMixin earlier in the Method Resolution Order so override
      methods of parent class.
    """

    def startDrag(self):
        data = cPickle.dumps(self.model())
        mimeData = QMimeData()
        mimeData.setData(LC_MIME_FORMAT, data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.start(Qt.CopyAction)

    def mouseMoveEvent(self, event):
        self.startDrag()
        QWidget.mouseMoveEvent(self, event)

class MiniVideoSceneWidget(DraggableMixin, QLabel):

    def __init__(self, parent):
        super(MiniVideoSceneWidget, self).__init__(parent)
        self.setText("Video Scene")

    def model(self):
        """
        :rtype: models.language.VideoScene
        """
        return language.VideoScene(
            "Example Video Scene",
            "Displays Gangnan Style video for 10 seconds from offset 0 seconds.",
            language.NumberValue(10),
            language.CommandSequence([]),
            language.CommandSequence([]),
            language.NumberValue(0),
            language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
        )

class MiniTextSceneWidget(DraggableMixin, QLabel):

    def __init__(self, parent):
        super(MiniTextSceneWidget, self).__init__(parent)
        self.setText("Text Scene")

    def model(self):
        """
        :rtype: models.language.TextScene
        """
        return language.TextScene(
            "Example Text Scene",
            "Displays title of Gangnan Style video for 10 seconds.",
            language.NumberValue(10),
            language.CommandSequence([]),
            language.CommandSequence([]),
            language.YoutubeVideoGetTitle(
                language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
            )
        )

class VideoSceneWidget(SceneWidget):

    def __init__(self, scene, parent):
        """
        :type scene: language.VideoScene
        """
        super(VideoSceneWidget, self).__init__(parent)

        self._comment = CommentWidget(scene.title + "\n" + scene.comment, self)
        self._comment.setMaximumHeight(50)
        self._preCommands = CommandSequenceWidget(scene.pre_commands, self)
        self._postCommands = CommandSequenceWidget(scene.post_commands, self)

        videoControls = QWidget(self)
        videoControlsLayout = QGridLayout()

        self._source = VideoGapWidget(scene.source, self)
        self._duration = NumberGapWidget(scene.duration, self)
        self._offset = NumberGapWidget(scene.offset, self)
        # self._volume = NumberGapWidget()

        videoControlsLayout.addWidget(QLabel("play"), 0, 0)
        videoControlsLayout.addWidget(self._source, 0, 1)
        videoControlsLayout.addWidget(QLabel("for"), 1, 0)
        videoControlsLayout.addWidget(self._duration, 1, 1)
        videoControlsLayout.addWidget(QLabel("from offset"), 2, 0)
        videoControlsLayout.addWidget(self._offset, 2, 1)
        # videoControlsLayout.addWidget(QLabel("at volume"), 3, 0)
        # videoControlsLayout.addWidget(self._volume, 3, 1)

        videoControls.setLayout(videoControlsLayout)

        layout = QVBoxLayout()
        layout.addWidget(self._comment)
        layout.addWidget(self._preCommands)
        layout.addWidget(videoControls)
        layout.addWidget(self._postCommands)

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
            self.source()
        )

    def offset(self):
        return self._duration.model()

    def source(self):
        return self._source.model()

class TextSceneWidget(SceneWidget):

    def __init__(self, scene, parent):
        """
        :type scene: TextScene
        """
        super(TextSceneWidget, self).__init__(parent)

        self._comment = CommentWidget(scene.title + "\n" + scene.comment, self)
        self._comment.setMaximumHeight(50)
        self._preCommands = CommandSequenceWidget(scene.pre_commands, self)
        self._postCommands = CommandSequenceWidget(scene.post_commands, self)

        textControls = QWidget(self)
        textControlsLayout = QGridLayout()

        self._text = TextGapWidget(scene.text, self)
        self._duration = NumberGapWidget(scene.duration, self)

        textControlsLayout.addWidget(QLabel("display"), 0, 0)
        textControlsLayout.addWidget(self._text, 0, 1)
        textControlsLayout.addWidget(QLabel("for"), 1, 0)
        textControlsLayout.addWidget(self._duration, 1, 1)

        textControls.setLayout(textControlsLayout)

        layout = QVBoxLayout()
        layout.addWidget(self._comment)
        layout.addWidget(self._preCommands)
        layout.addWidget(textControls)
        layout.addWidget(self._postCommands)

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

class CommandSequenceWidget(QWidget):
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
        self._layout.addWidget(self._gap)
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

    def _addAtEnd(self, widget):
        """
        Adds widget to end of layout but before gap.

        :type widget: QWidget
        """
        self._layout.insertWidget(self._layout.indexOf(self._gap), widget)

# TODO: Use live variables.
VARIABLE_NAMES = ["item", "curr_video", "curr_duration", "curr_offset"]

class GetWidget(DraggableMixin, QFrame):

    def __init__(self, getExpression, parent):
        """
        :type getExpression: language.GetVariableExpression
        """
        super(GetWidget, self).__init__(parent)

        self._name = QComboBox(self)
        for name in VARIABLE_NAMES:
            self._name.addItem(getExpression.name)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("get"))
        layout.addWidget(self._name)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.GetExpression
        """
        return language.GetVariableExpression(self._name.currentText())

class SetWidget(DraggableMixin, QFrame):

    def __init__(self, setStatement, parent):
        """
        :type setStatement: language.SetVariableStatement
        """
        super(SetWidget, self).__init__(parent)

        self._name = QComboBox()
        for name in VARIABLE_NAMES:
            self._name.addItem(setStatement.name)

        # Use empty NumberGapWidget for convenience.
        # TODO: Generalise.
        self._value = NumberGapWidget(setStatement.value, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("set"))
        layout.addWidget(self._name)
        layout.addWidget(QLabel("to"))
        layout.addWidget(self._value)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.SetVariableStatement
        """
        return language.SetVariableStatement(self._name.currentText(), self._value.model())

class TextValueWidget(DraggableMixin, QFrame):

    def __init__(self, text, parent):
        """
        :type text: language.TextValue
        """
        super(TextValueWidget, self).__init__(parent)
        self._text = QLineEdit(text.value, self)
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

class NumberValueWidget(DraggableMixin, QFrame):

    def __init__(self, number, parent):
        """
        :type number: language.NumberValue
        """
        super(NumberValueWidget, self).__init__(parent)
        self._number = QLineEdit(number.value, self)
        self._number.setValidator(QDoubleValidator())
        layout = QHBoxLayout()
        layout.addWidget(self._number)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.NumberValue
        """
        return language.NumberValue(float(self._number.text()))

class VideoValueWidget(DraggableMixin, QFrame):

    def __init__(self, video, parent):
        """
        :type video: language.VideoValue
        """
        super(VideoValueWidget, self).__init__(parent)
        self._value = QLineEdit(video.value, self)
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

class VideoCollectionDefnWidget(QWidget):

    def __init__(self, parent):
        super(VideoCollectionDefnWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        self.setGeometry(QRect(60, 160, 191, 71))
        self.setObjectName("widget_4")

        self.horizontalLayout_11 = QHBoxLayout(self)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.label_5 = QLabel(self)
        self.label_5.setText("")
        self.label_5.setPixmap(QPixmap("res/video-collection-64-64.png"))
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout_10.addWidget(self.lineEdit)

        self.horizontalLayout_11.addLayout(self.horizontalLayout_10)

class GapWidget(QStackedWidget):
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
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # self.setMinimumSize(QSize(10,10))
        self._child = None

        self.fillGap(child)

    def model(self):
        """
        :rtype: models.language.LanguageComponent
        """
        raise NotImplementedError

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(LC_MIME_FORMAT):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))
        self.fillGap(lc)

    def emptyGap(self):
        """
        Removes language compoment currently in gap.

        :raises RuntimeError: If gap is not currently occupied.
        """
        if not self.isFull():
            raise RuntimeError("Gap is currently not occupied.")

        # Remove from layout.
        # Ownership revert to application.
        self.removeWidget(self._child)
        # Delete that widgets making up the language subtree that had filled the gap.
        self._child.setParent(None)
        # Remove reference from GapWidget to the old child.
        self._child = None

    def fillGap(self, child):
        """
        Fills gap with language component, replacing language component
        currently occupying it.

        If component is a gap the gap will be emptied and left empty.

        :type child: language.LanguageComponent
        """
        if self.isFull():
            self.emptyGap()

        # Possible that language component might be a gap, in which case correct
        # behavior is to keep empty.
        if not isinstance(child, language.Gap):
            self._child = LanguageWidgetFactory.build(child, self)
            self.insertWidget(1, self._child)
            self.setCurrentIndex(1)

    def isFull(self):
        """
        :return: True if gap is currently occupied.
        :rtype: boolean
        """
        return self._child is not None

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
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(LC_MIME_FORMAT):
            event.accept()
        else:
            event.ignore()

class CommandGapWidget(ListGapWidget):

    def __init__(self, parent):
        """
        :param parent: Used to call back to for modifying commands.
        :type parent: CommandSequenceWidget
        """
        super(CommandGapWidget, self).__init__("drag command here", parent)

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))
        self.parent().addCommand(lc)

class SceneGapWidget(ListGapWidget):

    def __init__(self, parent):
        """
        :param parent: Used to call back to for modifying commands.
        :type parent: ActWidget
        """
        super(SceneGapWidget, self).__init__("drag text or video\nscene here", parent)

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))
        self.parent().addScene(lc)

class NumberOperatorWidget(DraggableMixin, QFrame):

    OPERATORS = {
        "+": language.Add,
        "-": language.Subtract,
        "/": language.Multiply
    }

    def __init__(self, operator, operand1, operand2, parent):
        """
        :type operator: string
        :type operand1: language.NumberExpression
        :type operand2: language.NumberExpression
        """

        assert operator in self.OPERATORS.keys()
        super(NumberOperatorWidget, self).__init__(parent)

        self._operand1 = NumberGapWidget(operand1, self)
        self._operand2 = NumberGapWidget(operand2, self)

        self._operator = QComboBox()
        self._operator.addItem("+")
        self._operator.addItem("-")
        self._operator.addItem("*")

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

class YoutubeVideoGetTitleWidget(DraggableMixin, QFrame):

    def __init__(self, videoGetTitle, parent):
        """
        :type videoGetTitle: language.YoutubeVideoGetTitle
        """

        super(YoutubeVideoGetTitleWidget, self).__init__(parent)

        self._video = VideoGapWidget(videoGetTitle.video, self)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("title of", self))
        layout.addWidget(self._video)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoGetTitle
        """
        return language.YoutubeVideoGetTitle(self._video.model())

class YoutubeVideoGetRelatedWidget(DraggableMixin, QFrame):

    def __init__(self, videoGetRelated, parent):
        """
        :type videoGetRelated: language.YoutubeVideoGetRelated
        """

        super(YoutubeVideoGetRelatedWidget, self).__init__(parent)

        self._video = VideoGapWidget(videoGetRelated.video, self)

        layout = QHBoxLayout()
        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-collection-64-64.png"))
        layout.addWidget(icon)
        layout.addWidget(QLabel("related to", self))
        layout.addWidget(self._video)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoGetRelated
        """
        return language.YoutubeVideoGetRelated(self._video.model())

class YoutubeVideoCollectionRandomWidget(DraggableMixin, QFrame):

    def __init__(self, videoCollectionRandom, parent):
        """
        :type videoCollectionRandom: language.YoutubeVideoCollectionRandom
        """

        super(YoutubeVideoCollectionRandomWidget, self).__init__(parent)

        self._videoCollection = VideoCollectionGapWidget(videoCollectionRandom.video_collection, self)

        layout = QHBoxLayout()
        icon = QLabel(self)
        icon.setPixmap(QPixmap("res/video-64-64.png"))
        layout.addWidget(icon)
        layout.addWidget(QLabel("random from", self))
        layout.addWidget(self._videoCollection)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.YoutubeVideoCollectionRandom
        """
        return language.YoutubeVideoCollectionRandom(self._videoCollection.model())