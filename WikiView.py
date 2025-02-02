'''
WikiView forms part of the MVC design model for the Wiki-Racing Application
Using the PyQt5 library to generate a GUI to allow players to play rounds of Wiki-Racing
Created by James Smith 31.1.2025
'''

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl, QTimer, QTime, QSize, QRect
from PyQt5.QtGui import *
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
import sys

DEFAULT_WINDOW_SIZE = QRect(300,300,800,600)
DEFAULT_FONT = QFont("MsGothic", 20)
WINDOW_TITLE = "Wiki-Racing"

'''
Name: MenuWindow
UI Elements: QVBoxLayout, QLabel, QPushButton 
Functions: start_game, start_game_random, show_leaderboard, show_settings
'''

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(DEFAULT_WINDOW_SIZE)
        layout = QVBoxLayout()
        menu_title = QLabel("Welcome to Wiki Racing")
        menu_title.setFont(DEFAULT_FONT)
        menu_title.setStyleSheet("color: white;")
        menu_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(menu_title)

        # Initialise buttons
        btn_play = QPushButton("Play")
        btn_play.setFont(DEFAULT_FONT)
        btn_play.clicked.connect(self.start_game)
        btn_play.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(btn_play)
        btn_leader = QPushButton("Leaderboard")
        btn_leader.setFont(DEFAULT_FONT)
        btn_leader.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;")
        btn_leader.clicked.connect(self.show_leaderboard)
        layout.addWidget(btn_leader)
        btn_quit = QPushButton("Quit")
        btn_quit.setFont(DEFAULT_FONT)
        btn_quit.setStyleSheet("background-color: #F44336; color: white; padding: 10px; border-radius: 5px;")
        btn_quit.clicked.connect(self.close_app)
        layout.addWidget(btn_quit)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")
        self.show()
    '''
    Method to start a specific round: Player defined start and end points
    '''

    def start_game(self):
        print("🎮 Play button clicked! Start game function here.")
        self.window = GameWindow()
        self.window.show()
        self.close()

    def show_leaderboard(self):
        print("Leaderboard button clicked! Leaderboard function here.")

    def close_app(self):
        print("❌ Quit button clicked! Closing application.")
        QApplication.quit()

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.time = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(DEFAULT_WINDOW_SIZE)
        layout = QVBoxLayout()
        game_title = QLabel("Wiki Racing!")
        game_title.setFont(DEFAULT_FONT)
        game_title.setStyleSheet("color: white;")
        layout.addWidget(game_title)
        lcd = QLCDNumber()
        lcd.setNumDigits(8)
        lcd.setSegmentStyle(QLCDNumber.Filled)
        lcd.resize(600, 200)
        self.timer = QTimer()
        self.time = QTime(0, 0, 0)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(10)
        lcd.display(self.time.toString('mm:ss.zzz'))
        layout.addWidget(lcd)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #222;")
        self.show()

    # Update the QLCDNumber object with current timing
    def show_time(self):
        self.time = self.time.addMSecs(10)
        self.lcd.display(self.time.toString('mm:ss.zzz'))


'''
Main Loop
Starts a QApplciation and loads the startMenu
Begins loop through app.exec_()
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Wiki Racing")
    menu = MenuWindow()
    sys.exit(app.exec_())