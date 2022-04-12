# Imports

import os
import sys
from typing import Text
from PyQt5 import QtCore

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


# Web Engine( pip install PyQtWebEngine)
from PyQt5.QtWebEngineWidgets import *
from PyQt5.sip import wrapper

# Main Window


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Add window elements
        # Add tab widgets to display web tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # Shortcut Key
        self.shortcutNewTab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcutNewTab.activated.connect(self.add_new_tab)

        # Add double click event listener
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # Add tab close event listener
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # Add active tab change event listener
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # Add navigation toolbar
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # Add buttons to navigation toolbar
        # Previous webpage button
        back_btn = QAction(
            QIcon(os.path.join('icons', 'cil-arrow-circle-left.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)

        # Navigate to previous  page
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        # Next webpage button
        next_btn = QAction(
            QIcon(os.path.join('icons', 'cil-arrow-circle-right.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)

        # Navigate to next webpage
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        # Refresh webpage button
        reload_btn = QAction(
            QIcon(os.path.join('icons', 'cil-reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)

        # Reload webpage
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload())

        # Home page button
        home_btn = QAction(
            QIcon(os.path.join('icons', 'cil-home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)

        # Navigate to default homepage
        home_btn.triggered.connect(self.navigate_home)

        # Add separation to navigation buttons
        navtb.addSeparator()

        # Add label icons to show the security status of the loaded url
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(
            QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)

        # Add the line edit to show and edit urls
        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)

        # Load url when enter button is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # Add stop button to stop url loading
        stop_btn = QAction(
            QIcon(os.path.join('icons', 'cil-media-stop.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        navtb.addAction(stop_btn)

        # Stop url loading
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        # new tab button
        tab_btn = QAction(
            QIcon(os.path.join('icons', 'cil-plus.png')), "New Tab", self)
        tab_btn.setStatusTip("New tab open")
        navtb.addAction(tab_btn)
        tab_btn.triggered.connect(lambda _: self.add_new_tab())

        # Add top menu
        # File menu
        file_menu = self.menuBar().addMenu("&File")

        # Add file menu actions
        new_tab_action = QAction(
            QIcon(os.path.join('icons', 'cil-library-add.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)

        # Homepage Navigation
        navigate_home_action = QAction(
            QIcon(os.path.join('icons', 'cil-exit-to-app.png')), "Homepage", self)
        navigate_home_action.setStatusTip("Go to Webnest Homepage")
        file_menu.addAction(navigate_home_action)
        navigate_home_action.triggered.connect(self.navigate_home)

        # Add new tabs
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())

        # Help menu
        # help_menu = self.menuBar().addMenu("&Help")

        # # Add help menu actions
        # navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')),
        #                                     "Homepage", self)
        # navigate_home_action.setStatusTip("Go to Sharda Design Homepage")
        # help_menu.addAction(navigate_home_action)

        # # Navigate to developer website
        # navigate_home_action.triggered.connect(self.navigate_home)

        # Set window title and icon
        self.setWindowTitle("Webnest Browser")
        self.setWindowIcon(
            QIcon(os.path.join('icons', 'web-browser-icon-small.png')))

        # Add stylesheet to customize your windows
        # Set stylesheet
        with open('style.css', "r") as style:
            self.setStyleSheet(style.read())

        # Load default homepage (google.com)
        # url = http://www.google.com,
        #label = Homepage
        # self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.add_new_tab(QUrl.fromLocalFile(
            os.path.abspath('index.html')), 'Homepage')
        # QtCore.QUrl.fromLocalFile(os.path.abspath('index.html'))

        # Show main window
        self.show()

    # ############################################
    # Functions
    ##############################################
    # Add new web tabs

    def add_new_tab(self, qurl=None, label="New Tab"):
        # Check if url value is blank
        if qurl is None:
            # qurl = QUrl('http://www.google.com')  # pass empty string to url

            qurl = QUrl.fromLocalFile(os.path.abspath('index.html'))

        # Load the passed url
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Add the webpage tab
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Add browser event listener
        # On URL change
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        # On loadfinished
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    # Add new tab on double click on tabs

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    # Close tabs
    def close_current_tab(self, i):
        if self.tabs.count() < 2:  # Only close if there is more than one tab open
            return

        self.tabs.removeTab(i)

    # Update url text when active tab is changed

    def update_urlbar(self, q, browser=None):
        # q = QURL
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return
        # URL Schema
        if q.scheme() == 'https':
            # If schema is https change icon to locked padlock to show that the webpage is secure
            self.httpsicon.setPixmap(
                QPixmap(os.path.join('icons', 'cil-lock-locked.png')))

        else:
            # If schema is not https change icon to locked padlock to show that the webpage is unsecure
            self.httpsicon.setPixmap(
                QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # Active tab change actions

    def current_tab_changed(self, i):
        # i = tab index
        # Get current tab url
        qurl = self.tabs.currentWidget().url()

        # Update url text
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # Update window title
        self.update_title(self.tabs.currentWidget())

    # Update window title

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current ACTIVE tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)

    # Navigate to passed url

    def navigate_to_url(self):  # Does not receive the Url
        # Get url text
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            # pass http as default url schema
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    # Navigate to default homepage

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl.fromLocalFile(os.path.abspath('index.html')))


app = QApplication(sys.argv)
# Application Name
app.setApplicationName("Webnest Browser")
# Application Company Name
app.setOrganizationName("Webnest Company")
# Application Company Organization
app.setOrganizationDomain("webnest.org")


window = MainWindow()
app.exec_()
