'''
Wiki Racing App - A standalone app for playing rounds of wiki racing and tracking scores
Created by James and Bruce Smith 21/11/2024
'''

# importing required libraries
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl, QTimer, QTime
from PyQt5.QtGui import *
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
import sys, csv
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
        self.add_browser(goal)
        self.startUrl = self.set_start(start)
        self.goalUrl = self.set_goal(goal)
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

    def add_browser(self, goal):
        self.browser = QWebEngineView()
        self.interceptor = WebEngineUrlRequestInterceptor()
        self.profile = QWebEngineProfile()
        self.profile.setUrlRequestInterceptor(self.interceptor)
        self.page = CustomWebPage(
            goal, self.stop_timer, self.profile, self.browser)
        self.browser.setPage(self.page)
        self.browser.setMinimumHeight(600)
        self.browser.setMinimumWidth(800)
        self.browser.resize(800, 600)
        self.browser.loadFinished.connect(self.update_title)
        # return browser

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

    def stop_timer(self):
        self.timer.stop()
        self.window = GameComplete(self.time)
        self.close()

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
Class to intercept every XHR call to load anything
This class is needed, though its sole method does nothing, because otherwise we get the runtime error:
TypeError: PyQt5.QtWebEngineCore.QWebEngineUrlRequestInterceptor represents a C++ abstract class and cannot be instantiated
'''

class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super(WebEngineUrlRequestInterceptor, self).__init__(parent)

    '''
    This method must be provided to avoid the runtime error:
    QWebEngineUrlRequestInterceptor.interceptRequest() is abstract and must be overridden
    '''

    def interceptRequest(self, _):
        x = 1  # dummy else Python is syntactically unhappy


'''
Class to restrict navigation to within Wikipedia
Checks for requests for pages outside of wikipedia as well as 
search requests made using the inbuilt wikipedia search bar
If either request is made, the request is ignored
'''

class CustomWebPage(QWebEnginePage):
    def __init__(self, goal, stopper, profile, parent=None):
        super(CustomWebPage, self).__init__(profile, parent)
        self.goal = goal.lower()
        self.stopper = stopper

    '''
    Method that checks every XHR request to ensure that only those going to Wikipedia destinations
    are processed. This holds the game player hostage on Wikipedia
    '''

    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        lower = url.toString().lower()
        if lower.find("wikipedia.org") < 0 or lower.find("wikipedia.org/w/index.php?search=") > 0:
            return False
        if lower.find(self.goal) > 0:
            self.stopper()
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
    '''

    def start_game(self):
        self.window = InputWindow()
        self.close()

    '''
    Method to begin a random round
    '''

    def start_game_random(self):
        self.window = CountdownTimer()
        self.window.show()
        self.close()

    def show_leaderboard(self):
        self.window = Leaderboard()
        self.window.show()
        self.close()


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
        opener = urllib.request.build_opener(NoRedirection)
        response = opener.open('https://en.wikipedia.org/wiki/Special:Random')
        location = response.getheader('Location')
        return location.removeprefix('https://en.wikipedia.org/wiki/')


'''
Name: NoRedirection
Description: A URL opener that does not follow redirections (HTTP 30x responses)
'''

class NoRedirection(urllib.request.HTTPErrorProcessor):
    def http_response(self, _, response):
        return response
    https_response = http_response

'''
Name: Leaderboard
Description: used to display player times stored in a csv file
TO BE IMPLEMENTED: Options for different score categories, the ability to return to menu
'''

class Leaderboard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(800,600)
        self.setWindowTitle("Leaderboard")
        self.central = QGraphicsView()
        self.grid = QVBoxLayout()
        self.title = QLabel("LeaderBoard")
        self.title.setFont(QFont("MS Gothic", 30))
        self.grid.addWidget(self.title)
        self.leaderboard = []
        self.read_leaderboard("leaderboard.csv")
        #print(self.leaderboard)
        for entry in self.leaderboard:
            print(entry[1])
            self.value = QLabel(f"{entry[0]}: {entry[1]}")
            self.value.setFont(QFont("MS Gothic", 20))
            self.grid.addWidget(self.value)
        self.btn_back = QPushButton("Back")
        self.grid.addWidget(self.btn_back)
        self.central.setLayout(self.grid)
        self.setCentralWidget(self.central)
        self.show()

    def read_leaderboard(self, filename):
        # Read the existing leaderboard from the CSV file
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    self.leaderboard.append((row[1], float(row[2])))  # Append name and time
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except ValueError:
            print("Error reading data. Ensure the CSV file has valid format.")

'''
Name: GameComplete
Description: Records the players time and takes input for a name to be used in the leaderboard
'''

class GameComplete(QMainWindow):
    def __init__(self, time, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Round Success")
        self.setGeometry(200,200,400,400)
        self.csvFile = "leaderboard.csv"
        self.leaderboard = []
        self.read_leaderboard()
        self.time = time

        # Create UI components
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label_player_name = QLabel("Enter Your Name: ")
        self.input_player_name = QLineEdit()
        self.label_time = QLabel("Your time was:")
        self.label_player_time = QLabel(self.time.toString('mm:ss.zzz'))
        self.btn_ok = QPushButton("Ok")
        self.btn_ok.clicked.connect(self.add_to_leaderboard)
        self.layout.addWidget(self.label_player_name)
        self.layout.addWidget(self.input_player_name)
        self.layout.addWidget(self.label_time)
        self.layout.addWidget(self.label_player_time)
        self.layout.addWidget(self.btn_ok)

        self.show()

    def read_leaderboard(self):
        # Read the existing leaderboard from the CSV file
        try:
            with open(self.csvFile, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    self.leaderboard.append((row[1], float(row[2])))  # Append name and time
        except FileNotFoundError:
            print(f"File '{self.csvFile}' not found.")
        except ValueError:
            print("Error reading data. Ensure the CSV file has valid format.")

    '''
    Utility method used to convert the QTime object into a float (seconds)
    '''
    def qtime_to_float(self):
        total_seconds = self.time.hour() * 3600 + self.time.minute() * 60 + self.time.second() + self.time.msec() / 1000.0
        return total_seconds

    '''
    Add the new player time into the "leaderboard.csv" file and sort in 
    '''
    def add_to_leaderboard(self):
        # Add the new entry to the leaderboard

        new_entry_name = self.input_player_name.text().strip()
        new_entry_time = self.qtime_to_float()

        if not new_entry_name:
            QMessageBox.warning(self, "Input Error", "Player name is required")
            return
        self.leaderboard.append((new_entry_name, new_entry_time))

        # Sort the leaderboard by time (ascending)
        self.leaderboard.sort(key=lambda x: x[1])

        # Save the updated leaderboard to the CSV file
        with open(self.csvFile, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Rank", "Name", "Time (seconds)"])  # Write headers
            for rank, (name, time) in enumerate(self.leaderboard, start=1):
                writer.writerow([rank, name, time])

        print(f"New entry added and leaderboard saved to '{self.csvFile}'!")
        self.window = MenuWindow()
        self.close()


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
