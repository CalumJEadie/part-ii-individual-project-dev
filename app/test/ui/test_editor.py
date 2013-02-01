"""
Integration tests for the editor.
"""

import unittest
import logging
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

    def setUp(self):
        self._app = _setup_qt()

    def test_editor(self):
        e = GraphicalEditor()
        self._app.exec_()

if __name__ == "__main__":
    unittest.main()