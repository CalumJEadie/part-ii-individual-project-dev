import sys
from PySide import QtGui

app = QtGui.QApplication(sys.argv) # every PySide app must an application object

wid = QtGui.QWidget() # base class for all UI objects in PySide
wid.resize(250, 150)
wid.setWindowTitle('Simple')
wid.show()

sys.exit(app.exec_()) # main loop
