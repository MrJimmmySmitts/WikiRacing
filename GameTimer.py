from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QLCDNumber, QApplication, QPushButton
from sys import argv, exit


class TimerWidget(QLCDNumber):
    def __init__(self, parent=None):
        super(TimerWidget, self).__init__(parent)

        self.setWindowTitle("Timer Widget")
        self.resize(800,600)
        self.setNumDigits(8)
        self.setSegmentStyle(QLCDNumber.Filled)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.time = QTime(0,0,0)
        timeDisplay = self.time.toString('mm:ss.zzz')
        self.display(timeDisplay)

        self.startButton = QPushButton(self)
        self.startButton.setText("Start")
        self.startButton.setGeometry(QtCore.QRect(150, 450, 200, 50))
        self.startButton.clicked.connect(self.initTimer)
        self.stopButton = QPushButton(self)
        self.stopButton.setText("Stop")
        self.stopButton.setGeometry(QtCore.QRect(450, 450, 200, 50))
        self.stopButton.clicked.connect(self.timer.stop)

    def initTimer(self):
        self.timer.start(10)
    def showTime(self):
        self.time = self.time.addMSecs(10)
        timeDisplay = self.time.toString('mm:ss.zzz')
        self.display(timeDisplay)




if __name__ == '__main__':
    app=QApplication(argv)
    frame = TimerWidget()
    frame.show()
    exit(app.exec_())