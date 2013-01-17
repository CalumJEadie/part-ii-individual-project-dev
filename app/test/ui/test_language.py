"""
Unit tests for language UI components.
"""

import unittest
import logging
from PySide import QtGui

from show import show

from app.ui.graphical_editor import *
from app.ui.language import *

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Test(unittest.TestCase):

    def test_editor(self):
        app = QtGui.QApplication([])
        e = GraphicalEditor()
        app.exec_()

    def test_act(self):
        app = QtGui.QApplication([])
        w = ActEdit()
        w.show()
        app.exec_()

    def test_scene(self):
        app = QtGui.QApplication([])
        w = SceneWidget()
        w.show()
        app.exec_()

    def test_video_slot(self):
        app = QtGui.QApplication([])
        w = VideoSlotWidget()
        w.show()
        app.exec_()

    def test_qobject_children(self):
        """
        Testing QObject.children().
        """
        app = QtGui.QApplication([])

        w1 = ActEdit()
        w1.show()
        show(w1.children())


        w2 = SceneWidget()
        w2.show()
        show(w2.children())

        w3 = CommandSequenceWidget()
        w3.show()
        show(w3.children())

    def test_act_model(self):
        app = QtGui.QApplication([])
        w = ActEdit()
        w.show()
        print w.model().translate()

    def test_text_value(self):
        app = QtGui.QApplication([])
        w = TextValueWidget("one")
        w.show()
        self.assertEqual(
            w.model().translate(),
            u"'one'"
        )
        print w.model().translate()
        app.exec_()

    def test_number_value(self):
        app = QtGui.QApplication([])
        w = NumberValueWidget(1.01)
        w.show()
        self.assertEqual(
            w.model().translate(),
            u"1.01"
        )
        print w.model().translate()
        app.exec_()

if __name__ == "__main__":
    unittest.main()