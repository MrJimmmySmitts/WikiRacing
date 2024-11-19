# importing required libraries
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import random
import sys

class CustomWebPage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if url.toString().lower().find("wikipedia.org") < 0:
            return False
        return super().acceptNavigationRequest(url,  _type, isMainFrame)


# creating main window class
class MainWindow(QMainWindow):

    def setUrl(self, url):
        self.browser.setUrl(QUrl(url))

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # creating a QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebPage(self))
        self.browser.setMinimumHeight(600)
        self.browser.setMinimumWidth(800)
        self.browser.resize(800,600)

        # setting default browser url as google
        # self.browser.setUrl(QUrl("https://www.wikipedia.org"))

        # adding action when url gets changed
        self.browser.urlChanged.connect(self.update_urlbar)

        # adding action when loading is finished
        self.browser.loadFinished.connect(self.update_title)

        # set this browser as central widget or main window
        self.setCentralWidget(self.browser)

        # creating a status bar object
        self.status = QStatusBar()

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")

        # adding this tool bar tot he main window
        self.addToolBar(navtb)

        # adding actions to the tool bar
        # creating a action for back
        back_btn = QAction("Back", self)

        # setting status tip
        back_btn.setStatusTip("Back to previous page")

        # adding action to the back button
        # making browser go back
        back_btn.triggered.connect(self.browser.back)

        # adding this action to tool bar
        navtb.addAction(back_btn)

        # similarly for forward action
        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")

        # adding action to the next button
        # making browser go forward
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # similarly for reload action
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")

        # adding action to the reload button
        # making browser to reload
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # similarly for home action
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # adding a separator in the tool bar
        navtb.addSeparator()

        # creating a line edit for the url
        self.urlbar = QLineEdit()

        # adding action when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # adding this to the tool bar
        navtb.addWidget(self.urlbar)

        # adding stop action to the tool bar
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")

        # adding action to the stop button
        # making browser to stop
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # showing all the components
        self.show()

    # method for updating the title of the window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - Wiki-Racing" % title)

    # method called by the home action
    def navigate_home(self):
        # open the google
        self.browser.setUrl(QUrl("https://www.wikipedia.org"))

    # method called by the line edit when return key is pressed
    def navigate_to_url(self):
        # getting url and converting it to QUrl object
        q = QUrl(self.urlbar.text())

        # if url is scheme is blank
        if q.scheme() == "":
            # set url scheme to html
            q.setScheme("http")

        # set the url to the browser
        if q.host().lower().find("wikipedia.org") > 0:
            self.browser.setUrl(q)

    # method for updating url
    # this method is called by the QWebEngineView object
    def update_urlbar(self, q):
        if q.toString().lower().find("wikipedia.org") > 0:
            # setting text to the url bar
            self.urlbar.setText(q.toString())

            # setting cursor position of the url bar
            self.urlbar.setCursorPosition(0)
'''
Name: MenuWindow
Attributes: titleLabel, playBtn, playRandBtn, settingsBtn, quitBtn
Methods: start_game, startgame_random, run_settings
'''
class MenuWindow(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Wiki-Racing")
        self.resize(600, 500)
        self.centralWidget = QLabel("Wiki Racing")
        self.centralWidget.setIndent(50)
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setCentralWidget(self.centralWidget)

        self.playBtn = QPushButton(self.centralWidget)
        self.playBtn.setGeometry(QtCore.QRect(200, 150, 200, 50))
        self.playBtn.setText("Play")
        self.playBtn.clicked.connect(self.start_game)

        self.playRandBtn = QPushButton(self.centralWidget)
        self.playRandBtn.setGeometry(QtCore.QRect(200, 250, 200, 50))
        self.playRandBtn.setText("Play Random")
        self.playRandBtn.clicked.connect(self.start_game_random)

        self.quitBtn = QPushButton(self.centralWidget)
        self.quitBtn.setGeometry(QtCore.QRect(200, 350, 200, 50))
        self.quitBtn.setText("Quit")
        self.quitBtn.clicked.connect(self.close)

        '''self.background = QGraphicsView(self.centralWidget)
        self.background.setGeometry(QtCore.QRect(0,0,600,500))
        self.background.'''

        self.show()
    def start_game(self):
        self.window = MainWindow()
        self.window.setUrl(urlman.start())
        self.window.show()
        self.hide()

    def start_game_random(self):
        self.window = MainWindow()
        self.window.setUrl("https://en.wikipedia.org/wiki/Special:Random")
        self.window.show()
        self.hide()


class URLManager:
    def __init__(self):
        self._starting_points = [
            "https://en.wikipedia.org/wiki/Rabbit",
            "https://en.wikipedia.org/wiki/Eucalypt",
            "https://en.wikipedia.org/wiki/Ferrari",
            ]
        self._end_points = [
            "https://en.wikipedia.org/wiki/Football",
            "https://en.wikipedia.org/wiki/England",
            "https://en.wikipedia.org/wiki/Climate_change",
            "https://en.wikipedia.org/wiki/Go_(programming_language)",
            ]
        self._start = random.randrange(0, len(self._starting_points))
        self._end = random.randrange(0, len(self._end_points))

    def start(self):
        return self._starting_points[self._start]
    
    def target(self):
        return self._end_points[self._end]


if __name__ == "__main__":
    # creating a pyQt5 application
    app = QApplication(sys.argv)
    # setting name to the application
    app.setApplicationName("Wiki Racing")
    # create a URL manager
    urlman = URLManager()
    # creating a main window object
    window = MenuWindow()
    # loop
    sys.exit(app.exec_())
