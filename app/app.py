import sys
from PySide import QtGui
import logging
import logging.config

import ui.editor

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    e = ui.editor.Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()