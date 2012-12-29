import sys
from PySide import QtGui

class Editor(QtGui.QWidget):
    
    def __init__(self):
        super(Editor, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.resize(800,600)
        self.setWindowTitle('Editor')

        qle = QtGui.QLineEdit(self)
        qle.move(50,50)

        svw = StringValueWidget(self)
        svw.move(50, 100)
    
        self.show()
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class StringValueWidget(QtGui.QLineEdit):

    def __init__(self, parent=None):
        super(StringValueWidget, self).__init__(parent)

        self.initUI()

    def initUI(self):

        self.setTextMargins(2,2,2,2)
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()