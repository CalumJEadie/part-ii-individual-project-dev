"""
Unit tests for language UI components.
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
        app = QtGui.QApplication([])
    except RuntimeError:
        app = QtCore.QCoreApplication.instance()

class Test(unittest.TestCase):

    def setUp(self):
        self._app = _setup_qt()

    def test_editor(self):
        e = GraphicalEditor()
        self._app.exec_()

    def test_act(self):
        w = ActEdit()
        w.show()
        self._app.exec_()

    def test_scene(self):
        w = SceneWidget()
        w.show()
        self._app.exec_()

    def test_video_slot(self):
        w = VideoSlotWidget()
        w.show()
        self._app.exec_()

    def test_qobject_children(self):
        """
        Testing QObject.children().
        """

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
        w = ActEdit()
        w.show()
        print w.model().translate()

    def test_text_value(self):
        w = TextValueWidget("one")
        w.show()
        self.assertEqual(
            w.model().translate(),
            u"'one'"
        )
        print w.model().translate()
        self._app.exec_()

    def test_number_value(self):
        w = NumberValueWidget(1.01)
        w.show()
        self.assertEqual(
            w.model().translate(),
            u"1.01"
        )
        print w.model().translate()
        self._app.exec_()

    def test_get_widget(self):
        w = GetWidget("item")
        w.show()
        print w.model().translate()
        self._app.exec_()

    def test_set_widget(self):
        w = SetWidget("item", VideoValue("http://www.youtube.com/watch?v=9bZkp7q19f0"))
        w.show()
        print w.model().translate()
        self._app.exec_()

class TestLanguageWidgetFactory(unittest.TestCase):

    def setUp(self):
        self._app = _setup_qt()

    def test_number_value(self):
        wf = LanguageWidgetFactory()
        m = NumberValue(1)
        w = wf.build(m)
        w.show()
        self.assertEqual(
            float(w.model().translate()),
            float(m.translate())
        )
        self._app.exec_()

    def test_text_value(self):
        wf = LanguageWidgetFactory()
        m = TextValue("one")
        w = wf.build(m)
        w.show()
        self.assertEqual(
            w.model().translate(),
            m.translate()
        )
        self._app.exec_()

    def test_number_operator(self):
        wf = LanguageWidgetFactory()
        m = Add(
            NumberValue(1),
            Subtract(
                NumberValue(2),
                NumberValue(3)
            )
        )
        w = wf.build(m)
        w.show()
        print w.model().translate()
        self._app.exec_()

class TestNumberOperatorBug(unittest.TestCase):
    """
    Attempting to recreate a bug occuring in LanguageWidgetFactory.build

    FIXED: Wasn't handling unmatched type, including Subtract.
    """

    def setUp(self):
        self._app = _setup_qt()

    def test(self):
        wf = LanguageWidgetFactory()
        m = Add(
            NumberValue(1),
            Subtract(
                NumberValue(2),
                NumberValue(3)
            )
        )
        w = wf.build(m._op2) # Seg fault was occuring on building op2
        w.show()

        self._app.exec_()

if __name__ == "__main__":
    unittest.main()