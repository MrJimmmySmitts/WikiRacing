import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton


class MenuWindow(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Wiki-Racing")
        self.resize(600, 400)
        self.centralWidget = QLabel("Wiki Racing")
        self.centralWidget.setIndent(50)
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setCentralWidget(self.centralWidget)

        self.playBtn = QPushButton(self.centralWidget)
        self.playBtn.setGeometry(QtCore.QRect(200, 150, 200, 50))
        self.playBtn.setText("Play")
        self.playBtn.clicked.connect(self.close)

        self.quitBtn = QPushButton(self.centralWidget)
        self.quitBtn.setGeometry(QtCore.QRect(200, 250, 200, 50))
        self.quitBtn.setText("Quit")
        self.quitBtn.clicked.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MenuWindow()
    win.show()
    sys.exit(app.exec_())