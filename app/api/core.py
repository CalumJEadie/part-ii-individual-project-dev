"""
Core API.
"""

import time
import logging
import random
import sys
from PySide import QtGui

from app.ui import core

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def display(text,duration):

    app = QtGui.QApplication(sys.argv)
    d = core.FullscreenDisplayDialogue(text)
    # d.exec_()
    time.sleep(duration)
    
    # QtGui.QMessageBox.information(None,"display",text,QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

    # sys.exit(app.exec_())

    # Quit QtCore.QCoreApplication.instance().quit

    # text = text[0:50]

    # logger.info("display(text=%s,duration=%s)",text,duration)
    # print text
    # time.sleep(duration)

def ask_yes_no(text):
    """
    :rtype: Boolean
    """

    choice = random.choice([True,False])
    logger.info("ask_yes_no(text=%s) = %s",text,choice)
    print text
    print choice
    return choice