import sys
from PySide import QtGui

class Editor(QtGui.QMainWindow):
    
    def __init__(self):
        super(Editor, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)

        self.statusBar()

        runAction = QtGui.QAction('Run', self)
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip('Run Program')
        runAction.triggered.connect(self.run)

        clearAction = QtGui.QAction('Clear', self)
        clearAction.setShortcut('Ctrl+E')
        clearAction.setStatusTip('Clear Program')
        clearAction.triggered.connect(self.clear)

        toolbar = self.addToolBar('Tools')
        toolbar.addAction(runAction)
        toolbar.addAction(clearAction)
        
        self.resize(800,600)
        self.center()
        self.setWindowTitle('Editor')    
        self.show()

        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    e = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
