from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QMainWindow, QLCDNumber, QVBoxLayout, QMessageBox, QApplication, QPushButton
from sys import argv, exit
from datetime import datetime

class TimerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self, parent)

        self.resize(800, 600)

        self.lcd = QLCDNumber(self)
        self.lcd.setNumDigits(8)
        self.timer = QTimer(self.lcd)
        #self.timer.timeout.connect(self.lcd_number)
        #self.lcd_number()
        self.currentTime = QTime(0, 0, 0)
        QVBoxLayout(self).addWidget(self.lcd)
        self.timer.start(1000)
        self.startButton = QPushButton(self)
        self.startButton.setText("Start")
        self.startButton.setGeometry(QtCore.QRect(150, 450, 200, 50))
        #self.startButton.clicked.connect(self.initTimer())
        self.startButton = QPushButton(self)
        self.startButton.setText("Stop")
        self.startButton.setGeometry(QtCore.QRect(450, 450, 200, 50))
        #self.startButton.clicked.connect(self.timer.stop())

    '''def lcd_number(self):
        time = datetime.now()
        formatted_time = time.strftime("%M:%S")
        self.lcd.setDigitCount(6)
        self.lcd.display(formatted_time)
'''
if __name__ == '__main__':
    app=QApplication(argv)
    frame=TimerWindow()
    frame.show()
    frame.raise_()
    exit(app.exec_())