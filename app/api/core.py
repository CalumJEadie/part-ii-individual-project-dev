"""
Core API.
"""

import time
import logging
from PySide import QtGui

from app.ui import core

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def display(text,duration):

    logger.info("display(text=%s,duration=%s)",text,duration)

    # app = QtGui.QApplication([])
    d = core.FullscreenDisplayDialog(text)
    time.sleep(duration)

def ask_yes_no(text):
    """
    :rtype: Boolean
    """
    
    # app = QtGui.QApplication([])
    choice = core.FullscreenBooleanDialog.getBoolean(text)
    logger.info("ask_yes_no(text=%s) = %s",text,choice)
    return choice