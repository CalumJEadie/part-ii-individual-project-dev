import sys
import logging
import argparse

import config
import ui.graphical_editor

def _ensure_dir_exists(dir_):
    """
    :type _dir: string
    """
    if not os.path.exists(dir_):
        os.makedirs(dir_)

def main():

    # Logging
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Prepare environment
    _ensure_dir_exists(config.APP_DIR)

    # Start Qt
    app = QtGui.QApplication(sys.argv)

    # Fire up graphical editor
    editor = ui.graphical_editor.GraphicalEditor()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()