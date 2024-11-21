'''
Wiki Racing App - A standalone app for playing rounds of wiki racing and tracking scores
Created by James and Bruce Smith 21/11/2024
'''

# importing required libraries
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys


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
Name: MainWindow
Attributes: browser, status, toolbar
Methods: add_to_toolbar, update_title, set_url
'''
class MainWindow(QMainWindow):
    # Initialise Browser window
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # initialising a QWebEngineView browser
        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebPage(self))
        self.browser.setMinimumHeight(600)
        self.browser.setMinimumWidth(800)
        self.browser.resize(800,600)
        self.browser.setUrl(QUrl("https://www.wikipedia.org"))
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

        # Initialising a status bar object
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

        # Initialising QToolBar for navigation
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


    # Updates the title of the browser window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Wiki-Racing" % title)

    # Sets the url using QUrl functionality
    def set_url(self, url):
        self.browser.setUrl(QUrl(url))


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
        self.resize(600, 500)
        self.centralWidget = QLabel("Wiki Racing")
        self.centralWidget.setIndent(50)
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setCentralWidget(self.centralWidget)

        # Initialise buttons
        # Play Button
        self.add_button(QtCore.QRect(200, 150, 200, 50), "Play", self.start_game)
        # Play Random Start, Random End Button
        self.add_button(QtCore.QRect(200, 250, 200, 50), "Play Random", self.start_game_random)
        # Quit Game Button
        self.add_button(QtCore.QRect(200, 350, 200, 50), "Quit", self.close)

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
        self.window = MainWindow()
        self.window.set_url("https://en.wikipedia.org/wiki/Special:Random")
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
