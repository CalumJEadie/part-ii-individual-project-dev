"""
Core API.
"""

import time
import logging
from PySide import QtGui, QtCore
import functools
from threading import Thread

from app.ui import core

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def display(text,duration):

    logger.info("display(text=%s,duration=%s)",text,duration)

    app = _initialise_qt()
    # dialog = core.FullscreenDisplayDialog(text)
    core.FullscreenDisplayDialog.display(text, duration)

    # Close after duration
    # QtCore.QTimer.singleShot(duration*1000, d.close)

    # dialog.exec_()

    # app.exec_()
    # time.sleep(duration)

def display_loading():
    """
    Display a loading message. Returns widget which can be closed using
    .close()

    :rtype: FullscreenDisplayDialog
    """

    logger.info("display_loading")

    app = _initialise_qt()
    dialog = core.FullscreenDisplayDialog("loading...")

    # Run event loop in another thread.
    Thread(target=dialog.exec_).start()

    # Problem, if display_loading is not followed by a display() call
    # the loading screen does not display.
    # Call display as a work around.
    display("", 0)
        
    return dialog

def ask_yes_no(text):
    """
    :rtype: Boolean
    """
    
    app = _initialise_qt()

    choice = core.FullscreenBooleanDialog.getBoolean(text)
    logger.info("ask_yes_no(text=%s) = %s",text,choice)
    return choice

def _initialise_qt():
    try:
        app = QtGui.QApplication([])
    except RuntimeError:
        app = QtCore.QCoreApplication.instance()
    return app