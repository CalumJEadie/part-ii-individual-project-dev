# -*- coding: utf-8 -*-

"""
Unit tests for Core API.
"""

import unittest
import logging
from PySide import QtGui
import time

from app.api import core

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Test(unittest.TestCase):

    duration = 4

    app = QtGui.QApplication([])

    def test_display(self):

        # Test unicode support.
        core.display("Psy - Gangnam Style Official Music Video [HD] (강남스타일) M/V",self.duration)

    def test_ask_yes_no(self):

        # Test type.
        res = core.ask_yes_no("Question (yes/no)? Enter yes.")
        self.assertIsInstance(res,bool)
        self.assertTrue(res)
        res = core.ask_yes_no("Question (yes/no)? Enter no.")
        self.assertIsInstance(res,bool)
        self.assertFalse(res)

    def test_loading(self):

        loading_dialog = core.display_loading()
        time.sleep(2)
        core.display("message 1", 2)
        time.sleep(2)
        core.display("message 2", 2)
        time.sleep(2)
        loading_dialog.close()


if __name__ == "__main__":
    unittest.main()