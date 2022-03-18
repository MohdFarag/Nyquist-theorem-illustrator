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
        #self.createtoolBar()
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
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)
        # setting configuration options
        pg.setConfigOptions(antialias=True)

        # Outer Layout
        outerLayout = QVBoxLayout()

        ######### INIT GUI #########
        # Initialize tab screen
        tabs = QTabWidget()
        
        self.samplingTab = QWidget()
        self.composerTab = QWidget()

        self.samplingLayout()
        self.composerLayout()
        
        # Add tabs
        tabs.addTab(self.samplingTab,"Sampling")
        tabs.addTab(self.composerTab,"Composer")
        
        outerLayout.addWidget(tabs)
        ######### INIT GUI #########

        centralMainWindow.setLayout(outerLayout)

    # Sampling
    def samplingLayout(self):
        pass
    
    # Composer
    def composerLayout(self):
        composerLayout = QVBoxLayout()
        
        sinusoidalLayout = QHBoxLayout()
        
        controlPanelSinusoidal = QVBoxLayout()
        freqBox = QLineEdit(self)
        freqBox.setStyleSheet("font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        freqBox.setPlaceholderText("Frequency")

        magnitudeBox = QLineEdit(self)
        magnitudeBox.setStyleSheet("font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        magnitudeBox.setPlaceholderText("Magnitude")

        phaseBox = QLineEdit(self)
        phaseBox.setStyleSheet("font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        phaseBox.setPlaceholderText("Phase")

        plotButton = QPushButton("Plot")
        plotButton.setStyleSheet("font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: black; color: #fff")
        #plotButton.setIcon(QIcon("images/plot.svg"))
        #plotButton.clicked.connect(plot)

        controlPanelSinusoidal.addWidget(freqBox)
        controlPanelSinusoidal.addWidget(magnitudeBox)
        controlPanelSinusoidal.addWidget(phaseBox)
        controlPanelSinusoidal.addWidget(plotButton)
        
        # Sinusoidal plot
        Sinusoidalplot = Plot("Sinusoidal Plot")

        sinusoidalLayout.addLayout(controlPanelSinusoidal)
        sinusoidalLayout.addWidget(Sinusoidalplot)

        summitionLayout = QHBoxLayout()

        summitionPlot = Plot("Sinusoidal Plot")

        summitionLayout.addWidget(summitionPlot)

        composerLayout.addLayout(sinusoidalLayout)
        composerLayout.addLayout(summitionLayout)

        self.composerTab.setLayout(composerLayout)

    # Browse signal
    def browseSignal():
        pass

    def exit(self):
        exitDlg = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)
        if exitDlg == QMessageBox.Yes:
            sys.exit()