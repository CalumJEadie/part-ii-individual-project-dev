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

from show import show

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# class ActWidget(QListView):

#     def __init__(self, parent):
#         super(ActWidget, self).__init__(parent)

# class ActView(QListView):

#     def __init__(self, parent):
#         super(ActView, self).__init__(parent)
#         # self.setAcceptDrops(True)
#         self.setDragDropMode(QAbstractItemView.InternalMove)

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

    def build(self, lc, parent):
        """
        Returns language component widget for given language component
        model.

        Reverse of .model() in language component widgets.

        :type model: <:LanguageComponent
        :type parent: QWidget
        :rtype: <:QWidget
        """

        builders = {
            language.NumberGap: lambda lc, p: NumberGapWidget(None, p),
            language.TextGap: lambda lc, p: TextGapWidget(None, p),
            language.VideoGap: lambda lc, p: VideoGapWidget(None, p),
            language.NumberValue: lambda lc, p: NumberValueWidget(float(lc.translate()), p),
            language.Add: lambda lc, p: NumberOperatorWidget(
                "+",
                self.build(lc._op1, p),
                self.build(lc._op2, p),
                p
            ),
            language.Subtract: lambda lc, p: NumberOperatorWidget(
                "-",
                self.build(lc._op1, p),
                self.build(lc._op2, p),
                p
            ),
            language.Multiply: lambda lc, p: NumberOperatorWidget(
                "*",
                self.build(lc._op1, p),
                self.build(lc._op2, p),
                p
            ),
            language.TextValue: lambda lc, p: TextValueWidget(lc.translate()[1:-1], p), # Remove brackets
            language.VideoValue: lambda lc, p: VideoValueWidget(lc._web_url, p),
            language.GetVariableExpression: lambda lc, p: GetWidget(lc._name, p),
            language.SetVariableStatement: lambda lc, p: SetWidget(lc._name, self.build(lc._value, p), p),
            language.CommandSequence: lambda lc, p: CommandSequenceWidget(
                # Create widget for each command in language component model
                map(lambda command: self.build(command, p), lc._children),
                p
            ),
            language.TextScene: lambda lc, p: TextSceneWidget(p),
            language.VideoScene: lambda lc, p: VideoSceneWidget(
                lc._title,
                lc._comment,
                self.build(lc._duration, p),
                self.build(lc._pre_commands, p),
                self.build(lc._post_commands, p),
                self.build(lc._offset, p),
                self.build(lc._source, p),
                p
            ),
        }

        return builders[lc.__class__](lc, parent)

class ActEdit(QWidget):
    """
    Basic implementation of drag and drop. Append only.
    """

    def __init__(self, parent):
        super(ActEdit, self).__init__(parent)

        self._scenes = []
        self._gap = SceneGapWidget(self)

        self._layout = QVBoxLayout()
        self._layout.addSpacing(10)
        self._layout.addWidget(self._gap)
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

    changed = Signal(str)

    def addScene(self, scene):
        """
        :type scene: QWidget
        """
        self._addAtEnd(scene)
        self._scenes.append(scene)

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

class CommentWidget(QPlainTextEdit):

    def __init__(self, text, parent):
        super(CommentWidget, self).__init__(text, parent)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Qt.ScrollBarAsNeeded
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        fm = QFontMetrics(self.font())
        h = fm.height() * 1.6
        self.setMinimumHeight(h)

        self.setMaximumHeight(50)

# class DraggableMixin(object):
#     """
#     Provides draggable behavioir.

#     ( ) what is a class that uses a mixin called?

#     Interface:
#     - Must subclass QWidget.
#     - Must provide a model() -> language.LanguageComponent method.
#     """

#     def startDrag(self):
#         data = cPickle.dumps(self.model())
#         mimeData = QMimeData()
#         mimeData.setData(LC_MIME_FORMAT, data)
#         drag = QDrag(self)
#         drag.setMimeData(mimeData)
#         drag.start(Qt.CopyAction)

#     def mouseMoveEvent(self, event):
#         self.startDrag()
#         QWidget.mouseMoveEvent(self, event)

class MiniVideoSceneWidget(QLabel):

    def __init__(self, parent):
        super(MiniVideoSceneWidget, self).__init__(parent)
        self.setText("Video Scene")

    def model(self):
        """
        :rtype: models.language.VideoScene
        """
        return language.VideoScene(
            "Example Video Scene",
            "",
            language.NumberValue(10),
            language.CommandSequence([]),
            language.CommandSequence([]),
            language.NumberValue(0),
            language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")
        )

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

class MiniTextSceneWidget(QLabel):

    def __init__(self, parent):
        super(MiniTextSceneWidget, self).__init__(parent)
        self.setText("Text Scene")

    def model(self):
        """
        :rtype: models.language.TextScene
        """
        return language.TextScene(
            "Example Text Scene",
            "",
            language.NumberValue(10),
            language.CommandSequence([]),
            language.CommandSequence([]),
            language.TextValue("title of gangnam style")
        )

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

class VideoSceneWidget(SceneWidget):

    def __init__(self, title, comment, duration, preCommands, postCommands, offset, source, parent):
        """
        :type title: string
        :type comment: string
        :type duration: <:QWidget
        :type preCommands: CommandSequenceWidget
        :type postCommands: CommandSequenceWidget
        :type offset: <:QWidget
        :type source: <:QWidget
        """
        super(VideoSceneWidget, self).__init__(parent)

        self._comment = CommentWidget(title + "\n" + comment, self)
        self._comment.setMaximumHeight(50)
        self._preCommands = preCommands
        self._postCommands = postCommands

        videoControls = QWidget(self)
        videoControlsLayout = QGridLayout()

        self._source = VideoGapWidget(source, self)
        self._duration = NumberGapWidget(duration, self)
        self._offset = NumberGapWidget(offset, self)
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

    def __init__(self,parent):
        super(TextSceneWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        self._comment = CommentWidget("comment", self)
        self._comment.setMaximumHeight(50)
        self._preCommands = CommandSequenceWidget([], self)
        self._postCommands = CommandSequenceWidget([], self)

        textControls = QWidget(self)
        textControlsLayout = QGridLayout()

        self._text = TextGapWidget(None, self)
        self._duration = NumberGapWidget(None, self)

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
        :type commands: QWidget iterable
        """

        super(CommandSequenceWidget, self).__init__(parent)

        self._commands = commands
        self._gap = CommandGapWidget(self)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._gap)
        self.setLayout(self._layout)

    def model(self):
        """
        :rtype: models.language.CommandSequence
        """
        return language.CommandSequence(map(lambda w: w.model(), self._commands))

    def addCommand(self, command):
        """
        :type command: QWidget
        """
        self._addAtEnd(command)
        self._commands.append(command)

    def _addAtEnd(self, widget):
        """
        Adds widget to end of layout but before gap.

        :type widget: QWidget
        """
        self._layout.insertWidget(self._layout.indexOf(self._gap), widget)

# TODO: Use live variables.
VARIABLE_NAMES = ["item", "curr_video", "curr_duration", "curr_offset"]

class GetWidget(QFrame):

    def __init__(self, name, parent):
        """
        :type name: string
        """
        super(GetWidget, self).__init__(parent)

        self._name = QComboBox(self)
        for name in VARIABLE_NAMES:
            self._name.addItem(name)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("get"))
        layout.addWidget(self._name)

        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.GetExpression
        """
        return language.GetVariableExpression(self._name.currentText())

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

class SetWidget(QFrame):

    def __init__(self, name, value, parent):
        """
        :type name: string
        :type value: QWidget
        """
        super(SetWidget, self).__init__(parent)

        self._name = QComboBox()
        for name in VARIABLE_NAMES:
            self._name.addItem(name)

        # Use empty NumberGapWidget for convenience.
        # TODO: Generalise.
        self._value = NumberGapWidget(None, self)

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

class TextValueWidget(QFrame):

    def __init__(self, text, parent):
        super(TextValueWidget, self).__init__(parent)
        self._text = QLineEdit(text, self)
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

class NumberValueWidget(QFrame):

    def __init__(self, number, parent):
        super(NumberValueWidget, self).__init__(parent)
        self._number = QLineEdit(str(number), self)
        self._number.setValidator(QDoubleValidator())
        layout = QHBoxLayout()
        layout.addWidget(self._number)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.NumberValue
        """
        return language.NumberValue(float(self._number.text()))

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

class VideoValueWidget(QFrame):

    def __init__(self, video, parent):
        super(VideoValueWidget, self).__init__(parent)
        self._value = QLineEdit(video, self)
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
        self._child = child

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

        wf = LanguageWidgetFactory()
        self._child = wf.build(lc, self)
        self.insertWidget(1, self._child)
        self.setCurrentIndex(1)

class NumberGapWidget(GapWidget):

    def __init__(self, child, parent):
        super(NumberGapWidget, self).__init__(child, parent)
        label = QLabel("number", self)
        self.addWidget(label)

    def model(self):
        """
        :rtype: models.language.NumberExpression
        """
        if self._child is not None:
            return self._child.model()
        else:
            return language.NumberGap()

class TextGapWidget(GapWidget):

    def __init__(self, child, parent):
        super(TextGapWidget, self).__init__(child, parent)
        label = QLabel("text", self)
        self.addWidget(label)

    def model(self):
        """
        :rtype: models.language.TextExpression
        """
        if self._child is not None:
            return self._child.model()
        else:
            return language.TextGap()

class VideoGapWidget(GapWidget):

    def __init__(self, child, parent):
        super(VideoGapWidget, self).__init__(child, parent)
        label = QLabel(self)
        label.setPixmap(QPixmap("res/video-64-64.png"))
        self.addWidget(label)

    def model(self):
        """
        :rtype: models.language.VideoExpression
        """
        if self._child is not None:
            return self._child.model()
        else:
            return language.VideoGap()

class CommandGapWidget(GapWidget):

    def __init__(self, parent):
        """
        :param parent: Used to call back to for modifying commands.
        :type parent: CommandSequenceWidget
        """

        super(CommandGapWidget, self).__init__(None, parent)
        label = QLabel("drag command here", self)
        self.addWidget(label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(LC_MIME_FORMAT):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))

        wf = LanguageWidgetFactory()
        self.parent().addCommand(wf.build(lc, self))

class SceneGapWidget(GapWidget):

    def __init__(self, parent):
        """
        :param parent: Used to call back to for modifying commands.
        :type parent: ActEdit
        """

        super(SceneGapWidget, self).__init__(None, parent)
        label = QLabel("drag scene here", self)
        self.addWidget(label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(LC_MIME_FORMAT):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))

        wf = LanguageWidgetFactory()
        self.parent().addScene(wf.build(lc, self))

class NumberOperatorWidget(QFrame):

    OPERATORS = {
        "+": language.Add,
        "-": language.Subtract,
        "/": language.Multiply
    }

    def __init__(self, operator, operand1, operand2, parent):
        """
        :type operator: string
        :type operand1: QWidget
        :type operand2: QWidget
        """

        assert operator in self.OPERATORS.keys()
        super(NumberOperatorWidget, self).__init__(parent)

        self._operand1 = operand1
        self._operand2 = operand2

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