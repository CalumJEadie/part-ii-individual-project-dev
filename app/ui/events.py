from PySide import QtCore

# Need to a static cast - PySide / Qt C++ weirdness
# http://permalink.gmane.org/gmane.comp.lib.qt.pyside/1813
ScriptChangeType = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

class ScriptChangeEvent(QtCore.QEvent):

    def __init__(self):
        super(ScriptChangeEvent, self).__init__(ScriptChangeType)