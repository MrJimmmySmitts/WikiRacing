from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel
from PyQt5 import uic
import sys

class StartMenu(QMainWindow):
    def __init__(self):
        super(StartMenu, self).__init__()

        # Load the UI Design File
        uic.loadUi("MenuDesign.ui", self)

        # Show the App
        self.show()


# Initialise the App
app = QApplication(sys.argv)
UIWindow = StartMenu()
app.exec()