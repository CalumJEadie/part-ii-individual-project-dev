"""
Core UI.
"""

from PySide import QtGui, QtCore

class FullscreenDisplayDialogue(QtGui.QWidget):
    
    def __init__(self,text):

        super(FullscreenDisplayDialogue, self).__init__()
        self.setupUI(text)
        self.show()

    def setupUI(self,text):

        grid = QtGui.QGridLayout(self)

        label = QtGui.QLabel(text,self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        label.setMargin(200)
        font = QtGui.QFont("serif",40)
        label.setFont(font)

        grid.addWidget(label)

        self.setLayout(grid)

        self.setStyleSheet("background: black; color: white;")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()

    #     self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    #     screenRect = QtGui.QDesktopWidget().screenGeometry()
    #     self.resize(screenRect)

    #     
        
    # def center(self):
        
    #     qr = self.frameGeometry()
    #     cp = QtGui.QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())




    # i(self, Form):
    #     Form.setObjectName(_fromUtf8("Form"))
    #     Form.resize(626, 402)
    #     self.gridLayout_2 = QtGui.QGridLayout(Form)
    #     self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    #     self.gridLayout = QtGui.QGridLayout()
    #     self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    #     self.label = QtGui.QLabel(Form)
    #     self.label.setAlignment(QtCore.Qt.AlignCenter)
    #     self.label.setWordWrap(True)
    #     self.label.setObjectName(_fromUtf8("label"))
    #     self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
    #     self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

    #     self.retranslateUi(Form)
    #     QtCore.QMetaObject.connectSlotsByName(Form)

    # def retranslateUi(self, Form):
    #     Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
    #     self.label.setText(QtGui.QApplication.translate("Form", "dfjnfksdjf kjasdfjk dsakfjdjksfkjsadkjadksadjkshksdhf dhskfdjksfhkjdkjdhskjfksdkdzfdksjhfksjhfkjsdf ", None, Q