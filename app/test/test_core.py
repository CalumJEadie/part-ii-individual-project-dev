# -*- coding: utf-8 -*-

"""
Unit tests for Core API.
"""

import unittest
import logging

from app.api import core

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Test(unittest.TestCase):

    def test_display(self):

        # Test unicode support.
        core.display("Psy - Gangnam Style Official Music Video [HD] (강남스타일) M/V",1)

    def test_ask_yes_no(self):

        # Test type.
        res = core.ask_yes_no("Question (yes/no)? Enter yes.")
        self.assertIsInstance(res,bool)
        res = core.ask_yes_no("Question (yes/no)? Enter no.")
        self.assertIsInstance(res,bool)

if __name__ == "__main__":
    unittest.main()
