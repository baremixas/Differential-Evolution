from GUI import *
import sys
from PySide6.QtWidgets import QApplication
from math import tan, atan, e, pi


#MAIN LOOP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec())
