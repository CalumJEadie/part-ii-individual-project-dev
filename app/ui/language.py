from PySide import QtGui,QtCore

class SceneWidget(QtGui.QWidget):

    def __init__(self,parent=None):
        super(SceneWidget, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(QtCore.QRect(20, 30, 251, 141))
        self.setStyleSheet("border: 1px solid purple")

        self.gridLayout_2 = QtGui.QGridLayout(self)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.gridLayout = QtGui.QGridLayout()

        self.label_6 = QtGui.QLabel("post instructions",self)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.plainTextEdit = QtGui.QPlainTextEdit("this is a space for secondary notation",self)


        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel("pre instructions",self)
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_7 = QtGui.QLabel("main scene",self)
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

class VideoDefnWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(VideoDefnWidget, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(QtCore.QRect(60, 30, 211, 71))
        self.setStyleSheet("background:red")
        self.setObjectName("widget_3")

        self.horizontalLayout_9 = QtGui.QHBoxLayout(self)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")

        self.label_4 = QtGui.QLabel(self)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("res/video-64-64.png"))
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.lineEdit_2 = QtGui.QLineEdit(self)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.horizontalLayout_8.addWidget(self.lineEdit_2)

        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)

class VideoCollectionDefnWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(VideoCollectionDefnWidget, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(QtCore.QRect(60, 160, 191, 71))
        self.setStyleSheet("background:red")
        self.setObjectName("widget_4")

        self.horizontalLayout_11 = QtGui.QHBoxLayout(self)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")

        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.label_5 = QtGui.QLabel(self)
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("res/video-collection-64-64.png"))
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout_10.addWidget(self.lineEdit)

        self.horizontalLayout_11.addLayout(self.horizontalLayout_10)

class GetterWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(GetterWidget, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
    
        self.setMaximumSize(QtCore.QSize(16777215, 71))
        self.setStyleSheet("background:white")
        self.setObjectName("widget_2")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.label_2 = QtGui.QLabel("get",self)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_2 = QtGui.QComboBox(self)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_5.addWidget(self.comboBox_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(spacerItem)

        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

class SetterWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(SetterWidget, self).__init__(parent)
        self.setupUI()

    def setupUI(self):

        self.setMaximumSize(QtCore.QSize(16777215, 51))
        self.setAutoFillBackground(False)
        self.setStyleSheet("background:white;")
        self.setObjectName("widget")

        self.horizontalLayout_4 = QtGui.QHBoxLayout(self)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label = QtGui.QLabel("set",self)
        self.label.setObjectName("label")

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.setObjectName("comboBox")

        self.horizontalLayout_3.addWidget(self.comboBox)

        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)