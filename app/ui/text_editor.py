from PySide import QtGui
import os.path
from os.path import join

from interpreter import interpreter

class TextEditor(QtGui.QMainWindow):

    d = os.path.dirname(__file__)
    example1 = open(join(d,"example1.py")).read()
    example2 = open(join(d,"example2.py")).read()
    
    def __init__(self):
        super(TextEditor, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        self.textEdit = QtGui.QPlainTextEdit()
        self.setCentralWidget(self.textEdit)

        self.statusBar()

        runAction = QtGui.QAction('Run', self)
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip('Run Program')
        runAction.triggered.connect(self.run)

        clearAction = QtGui.QAction('Clear', self)
        clearAction.setShortcut('Ctrl+E')
        clearAction.setStatusTip('Clear Program')
        clearAction.triggered.connect(self.clear)

        loadExample1Action = QtGui.QAction('Load Example 1', self)
        loadExample1Action.setStatusTip('Replace current program with example 1')
        loadExample1Action.triggered.connect(self.loadExample1)

        loadExample2Action = QtGui.QAction('Load Example 2', self)
        loadExample2Action.setStatusTip('Replace current program with example 2')
        loadExample2Action.triggered.connect(self.loadExample2)

        toolbar = self.addToolBar('Tools')
        toolbar.addAction(runAction)
        toolbar.addAction(clearAction)
        toolbar.addAction(loadExample1Action)
        toolbar.addAction(loadExample2Action)
        
        self.resize(800,600)
        self.center()
        self.setWindowTitle('TextEditor')    
        self.show()

        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run(self):
        program = self.textEdit.toPlainText()
        interpreter.interpret(program)

    def clear(self):
        self.textEdit.clear()

    def loadExample1(self):
        self.textEdit.setPlainText(self.example1)

    def loadExample2(self):
        self.textEdit.setPlainText(self.example2)
