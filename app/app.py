import sys
from PySide import QtGui
import logging
import logging.config
import argparse

import ui.text_editor
import ui.graphical_editor

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Possible editors.
TEXT_EDITOR = "text"
GRAPHICAL_EDITOR = "graphical"
        
def main():

    # Process command line.
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--editor",default=TEXT_EDITOR,choices=[TEXT_EDITOR,GRAPHICAL_EDITOR],help="specifies type of editor")
    args = parser.parse_args(sys.argv[1:])

    # Start application
    app = QtGui.QApplication(sys.argv)
    if args.editor == TEXT_EDITOR:
        e = ui.text_editor.TextEditor()
    else:
        e = ui.graphical_editor.GraphicalEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()