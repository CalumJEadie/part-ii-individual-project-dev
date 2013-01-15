import sys
from PySide import QtGui, QtCore

from ui import language

class TitleEditor(QtGui.QMainWindow):

    def __init__(self):

        super(TitleEditor, self).__init__()

        titles = [
            "Display video title",
            "Display video description",
            "Play video",
            "Ask for user feedback"
        ]
        self._model = QtGui.QStringListModel(titles)

        self.setupUI()
        self.show()

    def setupUI(self):

        self.setupWindow()
        self.setupToolbar()
        self.setupCentralWidget()

    def setupWindow(self):

        self.resize(1024,800)
        self.center()
        self.setWindowTitle('Title Editor')
        
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setupToolbar(self):

        toolbar = self.addToolBar("Tools")

        addAction = QtGui.QAction("Add Title", self)
        addAction.triggered.connect(self.addTitle)
        toolbar.addAction(addAction)

        removeAction = QtGui.QAction("Remove Title", self)
        removeAction.triggered.connect(self.removeTitle)
        toolbar.addAction(removeAction)

    def setupCentralWidget(self):

        self._actView = language.ActView()
        self._actView.setModel(self._model)
        self.setCentralWidget(self._actView)

    def addTitle(self):

        row = self._model.rowCount()
        self._model.insertRows(row, 1)
        index = self._model.index(row, 0)
        self._actView.setCurrentIndex(index)
        self._actView.edit(index)

    def removeTitle(self):
        index = self._actView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self._model.data(self._model.index(row), QtCore.Qt.DisplayRole)
        if QtGui.QMessageBox.question(self, "Titles - Remove", 
            "Remove %s?" % name,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No) == QtGui.QMessageBox.No:

            return

        self._model.removeRows(row,1)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    e = TitleEditor()
    sys.exit(app.exec_())