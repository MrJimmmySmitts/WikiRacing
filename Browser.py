# importing required libraries
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys


'''
Class to restrict navigation to within Wikipedia
'''
class CustomWebPage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if url.toString().lower().find("wikipedia.org") < 0:
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

        self.add_to_toolbar('back_btn', "Back", "Back to previous page", self.browser.back)
        self.add_to_toolbar("next_btn", "Next", "Forward to next page", self.browser.forward)
        self.add_to_toolbar("reload_btn", "Reload", "Reload page", self.browser.reload)
        self.add_to_toolbar("stop_btn", "Stop", "Stop loading page", self.browser.stop)

        # showing all the componentsn
        self.show()
    def add_to_toolbar(self, btn_name, text, tip, action):
        self.btn_name = QAction(text, self)
        self.btn_name.setStatusTip(tip)
        self.btn_name.triggered.connect(action)
        self.toolbar.addAction(btn_name)


    # method for updating the title of the window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Wiki-Racing" % title)

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
        self.add_button("playBtn", QtCore.QRect(200, 150, 200, 50), "Play", self.start_game)
        # Play Random Start, Random End Button
        self.add_button("playRandBtn", QtCore.QRect(200, 250, 200, 50), "Play Random", self.start_game_random)
        # Quit Game Button
        self.add_button("quitBtn", QtCore.QRect(200, 350, 200, 50), "Play", self.close)

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
    def add_button(self, name, rect, text, action):
        self.name = QPushButton(self.centralWidget)
        self.name.setGeometry(rect)
        self.name.setText(text)
        self.name.clicked.connect(action)

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
        self.window.setUrl("https://en.wikipedia.org/wiki/Special:Random")
        self.window.show()
        self.hide()

'''
Main Loop
Starts a QApplciation and loads the startMenu
Begins loop through app.exec_()
'''
if __name__ == "__main__":
    # creating a pyQt5 application
    app = QApplication(sys.argv)
    # setting name to the application
    app.setApplicationName("Wiki Racing")
    # creating a main window object
    window = MenuWindow()
    # loop
    sys.exit(app.exec_())
