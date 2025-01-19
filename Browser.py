'''
Wiki Racing App - A standalone app for playing rounds of wiki racing and tracking scores
Created by James and Bruce Smith 21/11/2024
'''

# importing required libraries
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl, QTimer, QTime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys
import urllib.request


'''
Name: MainWindow
Attributes: browser, status, toolbar
Methods: add_to_toolbar, update_title, set_url
'''


class MainWindow(QMainWindow):
    # Initialise Browser window
    def __init__(self, start, goal, parent=None):
        super(MainWindow, self).__init__(parent)

        '''
        Initialising The primary window with the following:
        Toolbar: [Back, Next, Reload, Stop] 
        Central Widget:
        QGraphicsView 
            QTWebEngineView
            QLCDNumber
        '''
        # Central widget with QGraphicsView as the root and a QVBoxLayout
        self.central = QGraphicsView()
        self.vBox = QVBoxLayout()

        self.lcd = self.add_timer()
        self.vBox.addWidget(self.lcd)
        self.endPageLabel = QLabel("Your Goal Is: " + goal)
        self.endPageLabel.setAlignment(Qt.AlignCenter)
        self.endPageLabel.setFont(QFont("MS Gothic", 30))
        self.vBox.addWidget(self.endPageLabel, 0)
        self.startUrl = self.set_start(start)
        self.goalUrl = self.set_goal(goal)
        self.browser = self.add_browser()
        self.set_url(self.startUrl)
        self.vBox.addWidget(self.browser)
        self.central.setLayout(self.vBox)
        self.central.setMinimumHeight(800)
        self.central.setMinimumWidth(800)
        self.central.resize(800, 800)
        self.setCentralWidget(self.central)

        # Initialising a status bar object
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

        # Initialising a top toolbar as QToolBar object
        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)
        self.add_to_toolbar("Back", "Back to previous page", self.browser.back)
        self.add_to_toolbar("Next", "Forward to next page",
                            self.browser.forward)
        self.add_to_toolbar("Reload", "Reload page", self.browser.reload)
        self.add_to_toolbar("Stop", "Stop loading page", self.browser.stop)

        '''self.topDock = QDockWidget()
        self.addDockWidget(self.topDock)'''

        self.gameStarted = False

        self.show()
    '''
    Method to add navigation button to the toolbar
    Arguments:
    text - the label of the button
    tip - the tooltip that displays on hover
    action - the function to be performed on triggered
    '''

    def add_to_toolbar(self, text, tip, action):
        button = QAction(text, self)
        button.setStatusTip(tip)
        button.triggered.connect(action)
        self.toolbar.addAction(button)

    '''
    Method to create a browser via QTWebEngineView
    Returns a QTWebEngineView object
    '''

    def add_browser(self):
        browser = QWebEngineView()
        browser.setPage(CustomWebPage(self))
        browser.setMinimumHeight(600)
        browser.setMinimumWidth(800)
        browser.resize(800, 600)
        browser.loadFinished.connect(self.update_title)
        return browser

    def add_timer(self):
        lcd = QLCDNumber(self)
        lcd.setNumDigits(8)
        lcd.setSegmentStyle(QLCDNumber.Filled)
        lcd.resize(600, 200)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.time = QTime(0, 0, 0)
        lcd.display(self.time.toString('mm:ss.zzz'))
        # self.timer.start(10)
        return lcd

    # Update the QLCDNumber object with current timing
    def showTime(self):
        self.time = self.time.addMSecs(10)
        self.lcd.display(self.time.toString('mm:ss.zzz'))

    # Updates the title of the browser window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Wiki-Racing" % title)
        if not self.gameStarted:
            self.timer.start(10)
            self.gameStarted = True

    # Sets the url using QUrl functionality
    def set_url(self, url):
        self.browser.setUrl(QUrl(url))

    def set_start(self, start):
        startUrl = "https://en.wikipedia.org/wiki/" + start
        return startUrl

    def set_goal(self, goal):
        goalUrl = "https://en.wikipedia.org/wiki/" + goal
        self.endPageLabel.setText("Your Goal Is: " + goal)
        return goalUrl

    def convert_goal_readable(self):
        goal = self.goalUrl[30:]
        goal.capitalize()
        return goal


'''
Class to restrict navigation to within Wikipedia
Checks for requests for pages outside of wikipedia as well as 
search requests made using the inbuilt wikipedia search bar
If either request is made, the request is ignored
'''


class CustomWebPage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        lower = url.toString().lower()
        if lower.find("wikipedia.org") < 0 or lower.find("wikipedia.org/w/index.php?search=") > 0:
            return False
        return super().acceptNavigationRequest(url,  _type, isMainFrame)


'''
Name: MenuWindow
Attributes: centralWidget, playBtn, playRandBtn, settingsBtn, quitBtn
Methods: start_game, startgame_random, run_settings
'''


class MenuWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialise Menu Window, title and sizes
        self.setWindowTitle("Wiki-Racing")
        self.resize(800, 800)
        self.centralWidget = QLabel("Wiki Racing")
        self.centralWidget.setIndent(50)
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.centralWidget.setFont(QFont("MS Gothic", 20))
        self.setCentralWidget(self.centralWidget)

        # Initialise buttons
        # Play Button
        self.add_button(QtCore.QRect(300, 150, 200, 50),
                        "Play", self.start_game)
        # Play Random Start, Random End Button
        self.add_button(QtCore.QRect(300, 250, 200, 50),
                        "Play Random", self.start_game_random)
        # Start up Timer Widget [Placeholder till functionality is incorporated into MainWindow]
        self.add_button(QtCore.QRect(300, 350, 200, 50),
                        "Leaderboard", self.show_leaderboard)
        # Quit Game Button
        self.add_button(QtCore.QRect(300, 450, 200, 50), "Quit", self.close)

        '''self.background = QGraphicsView(self.centralWidget)
        self.background.setGeometry(QtCore.QRect(0,0,600,500))
        self.background.'''

        self.show()

    '''
    Method to add button widgets to the window
    Arguments: 
    name - string - name of button
    rect - QtCore.QRect - (x, y, width, height) of button
    text - string - text to display on button
    action - action to be performed on clicked event
    '''

    def add_button(self, rect, text, action):
        button = QPushButton(self.centralWidget)
        button.setGeometry(rect)
        button.setText(text)
        button.clicked.connect(action)

    '''
    Method to start a specific round: Player defined start and end points
    NOT IMPLEMENTED: start point, end point, timer, start round, end round
    Random used as a placeholder
    '''

    def start_game(self):
        self.window = InputWindow()
        self.close()

    '''
    Method to begin a random round
    NOT IMPLEMENTED: end point, timer, end round
    '''

    def start_game_random(self):
        self.window = CountdownTimer()
        self.window.show()
        self.close()

    '''
    NOT IMPLEMENTED:
    will read from a csv file and output to a table showing top scores
    will have options for different score categories and 
    the ability to return to menu
    '''

    def show_leaderboard(self):
        pass


'''
Name: InputWindow
Description: A small pop-up window that waits for user input 
for the start page and the goal for the game before starting a new game
option to return to main menu
'''


class InputWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialise InputWindow
        self.setWindowTitle("Choose your path")
        self.resize(400, 400)
        self.central = QGraphicsView()
        self.grid = QVBoxLayout()
        self.start, self.startEntered = QInputDialog.getText(
            self, "Start Page", "Enter a page to start: ")
        self.goal, self.goalEntered = QInputDialog.getText(
            self, "Goal", "Enter a goal: ")
        self.startLabel = QLabel("Start Page: " + self.start)
        self.startLabel.setFont(QFont("MS Gothic", 10))
        self.grid.addWidget(self.startLabel)
        self.goalLabel = QLabel("Goal Page: " + self.goal)
        self.goalLabel.setFont(QFont("MS Gothic", 10))
        self.grid.addWidget(self.goalLabel)
        self.startBtn = QPushButton(self.central)
        self.startBtn.setText("Start")
        self.startBtn.clicked.connect(self.start_game)
        self.grid.addWidget(self.startBtn)
        self.backBtn = QPushButton(self.central)
        self.backBtn.setText("Back")
        self.backBtn.clicked.connect(self.close)
        self.grid.addWidget(self.backBtn)
        self.central.setLayout(self.grid)
        self.setCentralWidget(self.central)
        self.show()

    def start_game(self):
        self.window = MainWindow(self.start, self.goal)
        self.window.show()
        self.close()


'''
Name: Countdown Timer [QLCDNumber]
Description: A small window that will display a time in seconds 
and count down until it reaches zero, whereupon it will load the main browser page
'''


class CountdownTimer(QLCDNumber):
    def __init__(self, parent=None):
        super(CountdownTimer, self).__init__(parent)

        self.setWindowTitle("Get Ready!")
        self.setNumDigits(1)
        self.resize(100, 100)
        self.setSegmentStyle(QLCDNumber.Filled)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.time = QTime(0, 0, 5)
        self.display(self.time.toString('s'))
        self.timer.start(1000)

    def showTime(self):
        self.time = self.time.addSecs(-1)
        self.display(self.time.toString('s'))
        if self.time == QtCore.QTime(0, 0, 0):
            self.start_game(self.special(), self.special())

    def start_game(self, start, goal):
        self.window = MainWindow(start, goal)
        self.window.show()
        self.close()

    def special(self):
        urllib.request.build_opener(NoRedirection)
        opener = urllib.request.build_opener(NoRedirection)
        response = opener.open('https://en.wikipedia.org/wiki/Special:Random')
        location = response.getheader('Location')
        return location.removeprefix('https://en.wikipedia.org/wiki/')


class NoRedirection(urllib.request.HTTPErrorProcessor):
    def http_response(self, _, response):
        return response
    https_response = http_response


'''
Main Loop
Starts a QApplciation and loads the startMenu
Begins loop through app.exec_()
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Wiki Racing")
    window = MenuWindow()
    sys.exit(app.exec_())
