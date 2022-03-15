# !/usr/bin/python

# import plotter.py class
from plotter import Plot

# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import QFileInfo

# importing numpy and pandas
import numpy as np
import pandas as pd

# importing pyqtgraph as pg
import pyqtgraph as pg
from pyqtgraph.dockarea import *

import sys

class Window(QMainWindow):
    """Main Window."""
    def __init__(self):
        
        """Initializer."""
        super().__init__()

        self.setWindowIcon(QIcon('images/icon.png'))
        
        # setting title
        self.setWindowTitle("Nyquist Theorem Illustrator")

        # UI contents
        self.createMenuBar()
        self.createtoolBar()
        self.initUI()
        
        # Status Bar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("font-size:13px; padding: 3px; color: black; font-weight:900")
        self.statusBar.showMessage("Welcome to our application...")
        self.setStatusBar(self.statusBar)

    # Menu
    def createMenuBar(self):

        # MenuBar
        menuBar = self.menuBar()
        
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        
        openFile = QAction("Open...",self)
        openFile.setShortcut("Ctrl+o")
        openFile.setStatusTip('Open a new signal')
        openFile.triggered.connect(self.browseSignal)

        fileMenu.addAction(openFile)

        quit = QAction("Exit",self)
        quit.setShortcut("Ctrl+q")
        quit.setStatusTip('Exit application')
        quit.triggered.connect(self.exit)
        
        fileMenu.addAction(quit)

        # Add file tab to the menu
        menuBar.addMenu(fileMenu)

    def createtoolBar(self):
        pass

    # GUI
    def initUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # setting configuration options
        pg.setConfigOptions(antialias=True)

        # Outer Layout
        outerLayout = QVBoxLayout()

        ######### INIT GUI #########

        


        # outerLayout.addWidget()
        ######### INIT GUI #########

        wid.setLayout(outerLayout)

    def browseSignal(self):
        pass

    def exit(self):
        exitDlg = QMessageBox.critical(self, 
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)
        if exitDlg == QMessageBox.Yes:
            sys.exit()