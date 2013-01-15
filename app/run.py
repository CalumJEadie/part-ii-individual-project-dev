import sys
from PySide import QtGui
import logging
import logging.config
import argparse

import ui.text_editor
import ui.graphical_editor
import ui.basic_graphical_editor
import ui.title_editor

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Possible editors.
TEXT_EDITOR = "text"
GRAPHICAL_EDITOR = "graphical"
BASIC_GRAPHICAL_EDITOR = "basic_graphical"
TITLE_EDITOR = "title"
        
def main():

    # Process command line.
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--editor",default=TEXT_EDITOR,choices=[TEXT_EDITOR, GRAPHICAL_EDITOR, BASIC_GRAPHICAL_EDITOR, TITLE_EDITOR],help="specifies type of editor")
    args = parser.parse_args(sys.argv[1:])

    # Start application
    app = QtGui.QApplication(sys.argv)
    if args.editor == TEXT_EDITOR:
        e = ui.text_editor.TextEditor()
    elif args.editor == GRAPHICAL_EDITOR:
        e = ui.graphical_editor.GraphicalEditor()
    elif args.editor == BASIC_GRAPHICAL_EDITOR:
        e = ui.basic_graphical_editor.BasicGraphicalEditor()
    else:
        e = ui.title_editor.TitleEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()