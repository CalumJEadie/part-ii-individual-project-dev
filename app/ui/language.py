"""
Representation of language components.

Follow naming conventions used in PySide.

- Getters omit get, setters include.
- lowerCamelCase for methods and variables.
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

#     def __init__(self, parent=None):
#         super(ActWidget, self).__init__(parent)

# class ActView(QListView):

#     def __init__(self, parent=None):
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

    def build(self, lc, parent=None):
        """
        Returns language component widget for given language component
        model.

        Reverse of .model() in language component widgets.

        :type model: <:LanguageComponent
        :type parent: QWidget
        :rtype: <:QWidget
        """

        builders = {
            language.NumberGap: lambda lc, p: NumberGapWidget(p),
            language.TextGap: lambda lc, p: TextGapWidget(p),
            language.VideoGap: lambda lc, p: VideoGapWidget(p),
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
        }

        return builders[lc.__class__](lc, parent)

        # if isinstance(lc, language.NumberGap):
        #     return NumberGapWidget(parent)
        # elif isinstance(lc, language.TextGap):
        #     return TextGapWidget(parent)
        # elif isinstance(lc, language.VideoGap):
        #     return VideoGapWidget(parent)
        # elif isinstance(lc, language.NumberValue):
        #     return NumberValueWidget(float(lc.translate()), parent)
        # elif isinstance(lc, language.Add):
        #     return NumberOperatorWidget(
        #         "+",
        #         self.build(lc._op1, parent),
        #         self.build(lc._op2, parent),
        #         parent
        #     )
        # elif isinstance(lc, language.Subtract):
        #     return NumberOperatorWidget(
        #         "-",
        #         self.build(lc._op1, parent),
        #         self.build(lc._op2, parent),
        #         parent
        #     )
        # elif isinstance(lc, language.Multiply):
        #     return NumberOperatorWidget(
        #         "*",
        #         self.build(lc._op1, parent),
        #         self.build(lc._op2, parent),
        #         parent
        #     )
        # elif isinstance(lc, language.TextValue):
        #     return TextValueWidget(lc.translate()[1:-1], parent) # Remove brackets
        # elif isinstance(lc, language.VideoValue):
        #     return VideoValueWidget(lc._web_url, parent)
        # else:
        #     raise NotImplementedError

class ActEdit(QWidget):

    def __init__(self, parent=None):
        super(ActEdit, self).__init__(parent)
        self._scenes = [
            TextSceneWidget(self),
            VideoSceneWidget(self)
        ]
        self._setupUI()

    def _setupUI(self):
        layout = QVBoxLayout()
        layout.addSpacing(10)
        for scene in self._scenes:
            layout.addWidget(scene)
        layout.addStretch(10)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.Act
        """
        return language.Act(map(lambda x: x.model(), self._scenes))

    def mousePressEvent(self,event):
        self.changed.emit(self.model().translate())

    changed = Signal(str)


class ActWidget(QWidget):

    def __init__(self, parent=None):
        super(ActWidget, self).__init__(parent)
        self._scenes = [
            VideoSceneWidget(self)
        ]
        self._setupUI()

    def _setupUI(self):
        layout = QVBoxLayout()
        for scene in self._scenes:
            layout.addWidget(scene)
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.Act
        """
        return language.Act(map(lambda x: x.model(), self._scenes))

class SceneWidget(QWidget):

    def __init__(self,parent=None):
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

    def __init__(self, text="", parent=None):
        super(CommentWidget, self).__init__(text, parent)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Qt.ScrollBarAsNeeded
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        fm = QFontMetrics(self.font())
        h = fm.height() * 1.6
        self.setMinimumHeight(h)

        self.setMaximumHeight(50)

class MiniVideoSceneWidget(QLabel):

    def __init__(self, parent=None):
        super(MiniVideoSceneWidget, self).__init__(parent)
        self.setText("Video Scene")

    def model():
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
            language.VideoScene("http://www.youtube.com/watch?v=9bZkp7q19f0")
        )

class VideoSceneWidget(SceneWidget):

    def __init__(self,parent=None):
        super(VideoSceneWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        self._comment = CommentWidget("comment", self)
        self._comment.setMaximumHeight(50)
        self._preCommands = CommandSequenceWidget(self)
        self._postCommands = CommandSequenceWidget(self)

        videoControls = QWidget(self)
        videoControlsLayout = QGridLayout()

        self._source = VideoGapWidget()
        self._duration = NumberGapWidget()
        self._offset = NumberGapWidget()
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

    def __init__(self,parent=None):
        super(TextSceneWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        self._comment = CommentWidget("comment", self)
        self._comment.setMaximumHeight(50)
        self._preCommands = CommandSequenceWidget(self)
        self._postCommands = CommandSequenceWidget(self)

        textControls = QWidget(self)
        textControlsLayout = QGridLayout()

        self._text = TextGapWidget()
        self._duration = NumberGapWidget()

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

    def __init__(self, parent=None):
        super(CommandSequenceWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
        layout = QVBoxLayout()
        for i in range(1,4):
            layout.addWidget(QLabel("command %s" % i, self))
        self.setLayout(layout)

    def model(self):
        """
        :rtype: models.language.CommandSequence
        """
        return language.CommandSequence()

# TODO: Use live variables.
VARIABLE_NAMES = ["item", "curr_video", "curr_duration", "curr_offset"]

class GetWidget(QFrame):

    def __init__(self, name, parent=None):
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

    def __init__(self, name, value, parent=None):
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
        self._value = NumberGapWidget(self)

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

    def __init__(self, text, parent=None):
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

    def __init__(self, number, parent=None):
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

    def __init__(self, video, parent=None):
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

    def __init__(self, parent=None):
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

    def __init__(self, parent=None):
        super(GapWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # self.setMinimumSize(QSize(10,10))
        self._child = None

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

    def __init__(self, parent=None):
        super(NumberGapWidget, self).__init__(parent)
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

    def __init__(self, parent=None):
        super(TextGapWidget, self).__init__(parent)
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

    def __init__(self, parent=None):
        super(VideoGapWidget, self).__init__(parent)
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

class NumberOperatorWidget(QFrame):

    OPERATORS = {
        "+": language.Add,
        "-": language.Subtract,
        "/": language.Multiply
    }

    def __init__(self, operator, operand1, operand2, parent=None):
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