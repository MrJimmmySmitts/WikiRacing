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
        self.setSegmentStyle(QLCDNumber.Filled)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(10)
        self.showTime()

        self.startButton = QPushButton(self)
        self.startButton.setText("Start")
        self.startButton.setGeometry(QtCore.QRect(150, 450, 200, 50))
        self.startButton.clicked.connect(self.timer.start)
        self.stopButton = QPushButton(self)
        self.stopButton.setText("Stop")
        self.stopButton.setGeometry(QtCore.QRect(450, 450, 200, 50))
        self.stopButton.clicked.connect(self.timer.stop)

    def showTime(self):
        time = QTime(0,0,0)
        timeDisplay = time.toString('mm:ss')
        self.display(timeDisplay)



if __name__ == '__main__':
    app=QApplication(argv)
    frame = TimerWidget()
    frame.show()
    frame.raise_()
    exit(app.exec_())