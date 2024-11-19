from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QMainWindow, QLCDNumber, QVBoxLayout, QMessageBox, QApplication
from sys import argv, exit

class TimerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self, parent)

        self.resize(800, 600)

        self.lcdNumber = QLCDNumber(self)
        self.lcdNumber.setNumDigits(8)

        QVBoxLayout(self).addWidget(self.lcdNumber)

        self.currentTime = QTime(0, 0, 0)
        self.lcdNumber.display(self.currentTime.toString('hh:mm:ss'))
        self.timerId = self.startTimer(1000)


    def timer_event(self, event):
        if not event.timerId() == self.timerId: return

        self.currentTime = self.currentTime.addSecs(1)
        self.lcdNumber.display(self.currentTime.toString('hh:mm:ss'))

        if self.currentTime == QTime(0, 0, 4):
            msgBox = QMessageBox(
                QMessageBox.Information,
                "iTimer",
                "Time Out!",
                parent=self)

            stopButton = msgBox.addButton("Stop", QMessageBox.ActionRole)
            ignoreButton = msgBox.addButton(QMessageBox.Ignore)
            stopButton.clicked.connect(lambda: self.killTimer(self.timerId))

            msgBox.show()
            msgBox.raise_()
if __name__ == '__main__':
    app=QApplication(argv)
    frame=TimerWindow()
    frame.show()
    frame.raise_()
    exit(app.exec_())