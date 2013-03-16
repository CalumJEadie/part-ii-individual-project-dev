"""
Profiling of the editor.

http://docs.python.org/2/library/profile.html
http://pymotw.com/2/profile/
"""

import unittest
import logging
import cProfile
from PySide import QtGui, QtCore

from show import show

from app.ui.graphical_editor import *
from app.ui.language import *
from app.models.language import *

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def _setup_qt():
    try:
        #app = QtGui.QApplication([])
        application = app.ui.core.Application([])
    except RuntimeError:
        application = QtCore.QCoreApplication.instance()
    return application

class Test(unittest.TestCase):

    def test_editor(self):

        app = _setup_qt()
        e = GraphicalEditor()

        # Explicitly build local context as app not in context
        # used by cProfile.run()
        cProfile.runctx("app.exec_()", globals(), {"app": app})

if __name__ == "__main__":
    unittest.main()