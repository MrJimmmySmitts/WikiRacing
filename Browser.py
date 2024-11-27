'''
Wiki Racing App - A standalone app for playing rounds of wiki racing and tracking scores
Created by James and Bruce Smith 21/11/2024
'''

# importing required libraries
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl, QTimer, QTime
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys


'''
Name: MainWindow
Attributes: browser, status, toolbar
Methods: add_to_toolbar, update_title, set_url
'''
class MainWindow(QMainWindow):
    # Initialise Browser window
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        '''
        Initialising The primary window with the following:
        Toolbar: [Back, Next, Reload, Stop] 
        Central Widget:
        QGraphicsView 
            QTWebEngineView
            TimerWidget
        '''
        # Central widget with QGraphicsView as the root and a QVBoxLayout
        self.central = QGraphicsView()
        self.vBox = QVBoxLayout()
        self.browser = self.add_browser()
        self.vBox.addWidget(self.browser)
        self.lcd = self.add_timer()
        self.vBox.addWidget(self.lcd)
        self.central.setLayout(self.vBox)
        self.central.setMinimumHeight(800)
        self.central.setMinimumWidth(800)
        self.central.resize(800,800)
        self.setCentralWidget(self.central)
                
        # Initialising a status bar object
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

        # Initialising a top toolbar as QToolBar object
        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)
        self.add_to_toolbar("Back", "Back to previous page", self.browser.back)
        self.add_to_toolbar("Next", "Forward to next page", self.browser.forward)
        self.add_to_toolbar("Reload", "Reload page", self.browser.reload)
        self.add_to_toolbar("Stop", "Stop loading page", self.browser.stop)

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
        lcd.resize(600,200)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.time = QTime(0,0,0)
        lcd.display(self.time.toString('mm:ss.zzz'))
        self.timer.start(10)
        return lcd

    # Update the QLCDNumber object with current timing
    def showTime(self):
        self.time = self.time.addMSecs(10)
        self.lcd.display(self.time.toString('mm:ss.zzz'))

    # Updates the title of the browser window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Wiki-Racing" % title)

    # Sets the url using QUrl functionality
    def set_url(self, url):
        self.browser.setUrl(QUrl(url))

    def set_end_url(self, url):
        self.endPoint = url


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
        self.setCentralWidget(self.centralWidget)

        # Initialise buttons
        # Play Button
        self.add_button(QtCore.QRect(300, 150, 200, 50), "Play", self.start_game)
        # Play Random Start, Random End Button
        self.add_button(QtCore.QRect(300, 250, 200, 50), "Play Random", self.start_game_random)
        # Start up Timer Widget [Placeholder till functionality is incorporated into MainWindow]
        self.add_button(QtCore.QRect(300, 350, 200, 50), "Timer Widget", self.start_timer)
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
        self.window = MainWindow()
        self.window.set_url("https://en.wikipedia.org/wiki/Special:Random")
        self.window.show()
        self.hide()

    '''
    Method to begin a random round
    NOT IMPLEMENTED: end point, timer, start round, end round
    '''
    def start_game_random(self):
        self.window = CountdownTimer()
        self.window.show()
        self.hide()

    def start_timer(self):
        self.window = TimerWidget()
        self.window.show()
        self.hide()

class TimerWidget(QWidget):
    def __init__(self, parent=None):
        super(TimerWidget, self).__init__(parent)

        self.resize(800,200)
        self.lcd = QLCDNumber(self)
        self.lcd.setNumDigits(8)
        self.lcd.setSegmentStyle(QLCDNumber.Filled)
        self.lcd.resize(800,150)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.time = QTime(0,0,0)
        self.lcd.display(self.time.toString('mm:ss.zzz'))

        self.startButton = QPushButton(self)
        self.startButton.setText("Start")
        self.startButton.setGeometry(QtCore.QRect(150, 155, 100, 40))
        self.startButton.clicked.connect(self.initTimer)
        self.stopButton = QPushButton(self)
        self.stopButton.setText("Stop")
        self.stopButton.setGeometry(QtCore.QRect(350, 155, 100, 40))
        self.stopButton.clicked.connect(self.timer.stop)
        self.backButton = QPushButton(self)
        self.backButton.setText("Menu")
        self.backButton.setGeometry(QtCore.QRect(550, 155, 100, 40))
        self.backButton.clicked.connect(self.back_to_menu)
        self.show()

    def initTimer(self):
        self.timer.start(10)
    def showTime(self):
        self.time = self.time.addMSecs(10)
        self.lcd.display(self.time.toString('mm:ss.zzz'))
    def back_to_menu(self):
        self.window = MenuWindow()
        self.window.show()
        self.hide()


class CountdownTimer(QLCDNumber):
    def __init__(self, parent=None):
        super(CountdownTimer, self).__init__(parent)

        self.setWindowTitle("Get Ready!")
        self.setNumDigits(1)
        self.resize(100,100)
        self.setSegmentStyle(QLCDNumber.Filled)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.time = QTime(0,0,5)
        self.display(self.time.toString('s'))
        self.timer.start(1000)

    def showTime(self):
        self.time = self.time.addSecs(-1)
        self.display(self.time.toString('s'))
        if self.time == QtCore.QTime(0,0,0):
            self.start_game("https://en.wikipedia.org/wiki/Special:Random", "https://en.wikipedia.org/wiki/Special:Random")

    def start_game(self, startUrl, endUrl):
        self.timer.stop()
        self.window = MainWindow()
        self.window.set_url(startUrl)
        self.window.show()
        self.hide()
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
