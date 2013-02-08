from PySide import QtCore

# Need to a static cast - PySide / Qt C++ weirdness
# http://permalink.gmane.org/gmane.comp.lib.qt.pyside/1813
ScriptChangeType = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

class ScriptChangeEvent(QtCore.QEvent):

    def __init__(self):
        super(ScriptChangeEvent, self).__init__(ScriptChangeType)

# LiveNumberVariablesChangeType = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

# class LiveNumberVariablesChangeEvent(QtCore.QEvent):

#     def __init__(self):
#         super(LiveNumberVariablesChangeEvent, self).__init__(LiveNumberVariablesChangeType)

# LiveTextVariablesChangeType = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

# class LiveTextVariablesChangeEvent(QtCore.QEvent):

#     def __init__(self):
#         super(LiveTextVariablesChangeEvent, self).__init__(LiveTextVariablesChangeType)

# LiveVideoVariablesChangeType = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

# class LiveVideoVariablesChangeEvent(QtCore.QEvent):

#     def __init__(self):
#         super(LiveVideoVariablesChangeEvent, self).__init__(LiveVideoVariablesChangeType)

# LiveVideoCollectionVariablesChangeType = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

# class LiveVideoCollectionVariablesChangeEvent(QtCore.QEvent):

#     def __init__(self):
#         super(LiveVideoCollectionVariablesChangeEvent, self).__init__(LiveVideoCollectionVariablesChangeType)