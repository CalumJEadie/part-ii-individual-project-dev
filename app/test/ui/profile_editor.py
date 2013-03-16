"""
Profiling of the editor.

http://docs.python.org/2/library/profile.html
http://pymotw.com/2/profile/
http://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script
"""

import unittest
import logging
import cProfile
from PySide import QtGui, QtCore
import tempfile
import pstats

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

        stat_file_path = tempfile.mkstemp(".pstats", prefix="evelyn_profile")[1]
        print stat_file_path
        # Explicitly build local context as app not in context
        # used by cProfile.run()
        cProfile.runctx("app.exec_()", globals(), {"app": app}, stat_file_path)
        stats = pstats.Stats(stat_file_path)

        # show by cumulative time - is the total time spent in this and all
        # subfunctions (from invocation till exit)
        stats.strip_dirs().sort_stats('cumulative').print_stats(40)

        # show by internal time - excl. some functions        
        stats.strip_dirs().sort_stats('time').print_stats(40)

if __name__ == "__main__":
    unittest.main()