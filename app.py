# !/usr/bin/python

# import Plotter.py Class
from turtle import Pen
import plotter
from plotter import Plot

# Definition of Main Color Palette
COLOR1 = plotter.COLOR1
COLOR2 = plotter.COLOR2
COLOR3 = plotter.COLOR3
COLOR4 = plotter.COLOR4

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

class TableView(QTableWidget):
    def __init__(self,*args):
        QTableWidget.__init__(self, *args)
        self.data = []	
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['Frequency','Magnitude','Phase'])
 
    def addData(self, frequency, magnitude, phase): 
        rowPosition = self.rowCount()

        self.insertRow(rowPosition)
        self.setItem(rowPosition , 0, QTableWidgetItem(f"{frequency} Hz"))
        self.setItem(rowPosition , 1, QTableWidgetItem(f"{magnitude}"))
        self.setItem(rowPosition , 2, QTableWidgetItem(f"{phase} °"))

    def getData(self):
        return self.data 

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
        self.statusBar.setStyleSheet(f"""font-size:13px;
                                 padding: 3px; 
                                 color: {COLOR1}; 
                                 font-weight:900;""")
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

        # Outer Layout
        outerLayout = QVBoxLayout()

        ######### INIT GUI #########
        # Initialize tab screen
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""color:{COLOR1}; 
                        font-size:15px;""")

        self.samplingTab = QWidget()
        self.samplingTab.setStyleSheet(f"""background: {COLOR4}""")
        self.composerTab = QWidget()
        self.composerTab.setStyleSheet(f"""background: {COLOR4}""")

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
        samplingLayout = QVBoxLayout()

        # Main Layout
        mainLayout = QVBoxLayout()
        
        # Main Plot
        mainplot = Plot("Main Plot")

        # Main Buttons Layout
        mainButtons = QHBoxLayout()

        # Sampling slider
        frequencyStartLabel = QLabel("0")
        frequencyStartLabel.setStyleSheet("font-size: 13px;padding: 2px;font-weight: 800;")
        sliderMainPlot = QSlider(Qt.Horizontal,self)
        frequencyEndLabel = QLabel(u'F\u2098\u2090\u2093')
        frequencyEndLabel.setStyleSheet("font-size: 13px;padding: 2px;font-weight: 800;")
        
        # Reconstruct signal type : dotted or secondary graph
        reconstructType = QComboBox()
        reconstructType.setStyleSheet(f"""font-size:14px;
                                    height: 25px;
                                    padding: 0px 5px;""")
        reconstructType.addItem("Choose")
        reconstructType.addItem("Secondary graph")
        reconstructType.addItem("Dotted signal")

        # Sampling Buttons
        plotButton = QPushButton("Reconstruct")
        plotButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")
 

        mainButtons.addWidget(frequencyStartLabel)
        mainButtons.addWidget(sliderMainPlot)
        mainButtons.addWidget(frequencyEndLabel)
        mainButtons.addWidget(reconstructType)
        mainButtons.addWidget(plotButton)

        mainLayout.addWidget(mainplot)
        mainLayout.addLayout(mainButtons)

        # Reconstraction layout
        reconstractionLayout = QVBoxLayout()
        
        # Reconstraction plot
        reconstractionPlot = Plot("Reconstraction Plot")

        # Reconstruction Buttons
        reconstructButtons = QHBoxLayout()

        reconstructButtons.addSpacerItem((QSpacerItem(30, 10, QSizePolicy.Expanding)))
        # Hide Button        
        hideButton = QPushButton("Hide Reconstraction Plot")
        hideButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")
        reconstructButtons.addWidget(hideButton)
        reconstructButtons.addSpacerItem((QSpacerItem(30, 10, QSizePolicy.Expanding)))
        
        reconstractionLayout.addWidget(reconstractionPlot)
        reconstractionLayout.addLayout(reconstructButtons)            

        samplingLayout.addLayout(mainLayout)
        samplingLayout.addLayout(reconstractionLayout) 

        self.samplingTab.setLayout(samplingLayout)
    
    # Composer Layout Tab
    def composerLayout(self):
        composerLayout = QVBoxLayout()
        
        # Sinusoidal Layout
        sinusoidalLayout = QHBoxLayout()
        
        panelGroupBox = QGroupBox("Panel")
        panelSinusoidal = QVBoxLayout()
        panelGroupBox.setLayout(panelSinusoidal)
        
        # Frequency Text Box
        freqBox = QLineEdit(self)
        freqBox.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR2};
                            color: {COLOR4};""")
        freqBox.setPlaceholderText("Frequency")

        # Magnitude Text Box
        magnitudeBox = QLineEdit(self)
        magnitudeBox.setStyleSheet(f"""font-size:14px; 
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px; 
                                background: {COLOR2};
                                color: {COLOR4};""")
        magnitudeBox.setPlaceholderText("Magnitude")

        # Phase Text Box
        phaseBox = QLineEdit(self)
        phaseBox.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR2};
                            color: {COLOR4};""")
        phaseBox.setPlaceholderText("Phase")

        plotButton = QPushButton("Plot")
        plotButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")
        # plotButton.setIcon(QIcon("images/plot.svg"))
        # plotButton.clicked.connect(plot)

        panelSinusoidal.addWidget(freqBox)
        panelSinusoidal.addWidget(magnitudeBox)
        panelSinusoidal.addWidget(phaseBox)
        panelSinusoidal.addWidget(plotButton)
        
        # Sinusoidal Plot
        Sinusoidalplot = Plot()

        sinusoidalLayout.addWidget(panelGroupBox,3)
        sinusoidalLayout.addWidget(Sinusoidalplot,7)

        # Summition Layout
        summitionLayout = QHBoxLayout()
        
        summitionGroupBox = QGroupBox("Panel")
        summitionSinusoidal = QVBoxLayout()
        summitionGroupBox.setLayout(summitionSinusoidal)
        
        # Table of signals
        signalsTable = TableView()
        
        # List of signale layout
        listLayout = QHBoxLayout()
        
        # Delete of signal button 
        deleteButton = QPushButton()

        # Reconstruct signal type : dotted or secondary graph
        signalsList = QComboBox()
        signalsList.setStyleSheet(f"""font-size:14px;
                                    height: 25px;
                                    padding: 0px 5px;""")
        signalsList.addItem("Choose...")
        
        # Delete of signal button 
        deleteButton = QPushButton()
        deleteButton.setIcon(QIcon("images/clear.svg"))
        deleteButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;""")
                            
        listLayout.addWidget(signalsList,4)
        listLayout.addWidget(deleteButton,1)

        confirmButton = QPushButton("Confirm")
        confirmButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")

        summitionSinusoidal.addWidget(signalsTable)
        summitionSinusoidal.addLayout(listLayout)
        summitionSinusoidal.addWidget(confirmButton)

        # Summition Plot  
        summitionPlot = Plot()

        summitionLayout.addWidget(summitionGroupBox, 3)
        summitionLayout.addWidget(summitionPlot ,7)

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
