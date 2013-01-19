from PySide.QtGui import *
from PySide.QtCore import *
import logging
import cPickle

from app.models import language

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

class GetterWidget(QWidget):

    def __init__(self, parent=None):
        super(GetterWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):
    
        self.setMaximumSize(QSize(16777215, 71))
        self.setObjectName("widget_2")
        self.horizontalLayout_6 = QHBoxLayout(self)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.label_2 = QLabel("get",self)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_5.addWidget(self.comboBox_2)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(spacerItem)

        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

class SetterWidget(QWidget):

    def __init__(self, parent=None):
        super(SetterWidget, self).__init__(parent)
        self._setupUI()

    def _setupUI(self):

        self.setMaximumSize(QSize(16777215, 51))
        self.setAutoFillBackground(False)
        self.setObjectName("widget")

        self.horizontalLayout_4 = QHBoxLayout(self)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label = QLabel("set",self)
        self.label.setObjectName("label")

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName("comboBox")

        self.horizontalLayout_3.addWidget(self.comboBox)

        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

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
        # TODO add validator
        
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
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self._child = None

    def model(self):
        """
        :rtype: models.language.Expression
        """
        if self._child is not None:
            return self._child.model()
        else:
            return language.Gap()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(LC_MIME_FORMAT):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        lc = cPickle.loads(str(event.mimeData().data(LC_MIME_FORMAT)))

        if isinstance(lc, language.NumberValue):
            self._child = NumberValueWidget(float(lc.translate()), self)
            self.insertWidget(1, self._child)
            self.setCurrentIndex(1)
        elif isinstance(lc, language.Add):
            self._child = NumberOperatorWidget("+", NumberGapWidget(), NumberGapWidget(), self)
            self.insertWidget(1, self._child)
            self.setCurrentIndex(1)
        elif isinstance(lc, language.TextValue):
            self._child = TextValueWidget(lc.translate(), self)
            self.insertWidget(1, self._child)
            self.setCurrentIndex(1)
        elif isinstance(lc, language.VideoValue):
            self._child = VideoValueWidget(lc.translate(), self)
            self.insertWidget(1, self._child)
            self.setCurrentIndex(1)

class NumberGapWidget(GapWidget):

    def __init__(self, parent=None):
        super(NumberGapWidget, self).__init__(parent)

class TextGapWidget(GapWidget):

    def __init__(self, parent=None):
        super(TextGapWidget, self).__init__(parent)

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
        return language.VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0")

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