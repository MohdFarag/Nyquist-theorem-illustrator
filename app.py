# !/usr/bin/python

# import Plotter.py Class
from signal import signal
from plotter import Plot
from plotterMatplotlib import MplCanvas

# Definition of Main Color Palette
from Defs import COLOR1,COLOR2,COLOR3,COLOR4, COLOR5

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
import os
from scipy.fft import rfft, fft, fftfreq

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

        # Initialize Variables
        self.mainDataPlot = []
        self.signalSummition = [0 for _ in range(0,1000)]
        self.hidden = False


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
        self.mainPlot = MplCanvas("Main Plot")

        ### Will be deleted ###
        x = np.linspace(-np.pi/2, np.pi/2, 1000)
        y1 = np.sin(2 * np.pi * 10 * x)
        y2 = np.sin(2 * np.pi * 1 * x + 90)
        y3 = np.sin(2 * np.pi * 3 * x + 270)
        y = y1 + y2 + y3

        self.mainPlot.set_data(y, x)
        
        self.mainPlot.plotDiscreteSignal()
        ### Will be deleted ###

        # Main Buttons Layout
        mainButtons = QHBoxLayout()

        # Sampling slider
        self.frequencyStartLabel = QLabel("1")
        self.frequencyStartLabel.setStyleSheet("font-size: 13px;padding: 2px;font-weight: 800;")

        sliderMainPlot = QSlider(Qt.Horizontal,self)
        sliderMainPlot.setMinimum(1)
        sliderMainPlot.setMaximum(3*1000)

        frequencyEndLabel = QLabel(u'3F\u2098\u2090\u2093')
        
        frequencyEndLabel.setText(frequencyEndLabel.text() + '= 3*500Hz')
        frequencyEndLabel.setStyleSheet("font-size: 13px;padding: 2px;font-weight: 800;")
        
        # Reconstruct signal type : dotted or secondary graph
        self.reconstructType = QComboBox()
        self.reconstructType.setStyleSheet(f"""font-size:14px;
                                    height: 25px;
                                    padding: 0px 5px;
                                    background: {COLOR4};
                                    color:{COLOR1};""")
        self.reconstructType.addItem("Choose")
        self.reconstructType.addItem("In Secondary graph")
        self.reconstructType.addItem("Dotted signal")

        # Sampling Buttons
        plotReconstructButton = QPushButton("Reconstruct")
        plotReconstructButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")
        plotReconstructButton.clicked.connect(self.reconstructSample)
 
        mainButtons.addWidget(self.frequencyStartLabel)
        mainButtons.addWidget(sliderMainPlot)
        mainButtons.addWidget(frequencyEndLabel)
        mainButtons.addWidget(self.reconstructType)
        mainButtons.addWidget(plotReconstructButton)

        mainLayout.addWidget(self.mainPlot)
        mainLayout.addLayout(mainButtons)

        
        # Reconstraction layout
        reconstructionLayout = QVBoxLayout()
        
        # Reconstraction plot
        self.reconstructedframe = QFrame()
        tempLayout = QHBoxLayout()
        self.reconstractionPlot = MplCanvas(title="Reconstraction Plot")
        tempLayout.addWidget(self.reconstractionPlot)
        self.reconstructedframe.setLayout(tempLayout)       

        sliderMainPlot.valueChanged[int].connect(self.freqChange)

        # Reconstruction Buttons
        reconstructButtons = QHBoxLayout()

        reconstructButtons.addSpacerItem((QSpacerItem(30, 10, QSizePolicy.Expanding)))
        # Hide Button        
        self.hideButton = QPushButton("Reconstraction Plot")
        self.hideButton.setIcon(QIcon("images/show.svg"))
        self.hideButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")
        self.hideButton.clicked.connect(self.hideSecGraph)

        reconstructButtons.addWidget(self.hideButton)
        reconstructButtons.addSpacerItem((QSpacerItem(30, 10, QSizePolicy.Expanding)))
        
        reconstructionLayout.addWidget(self.reconstructedframe)
        reconstructionLayout.addLayout(reconstructButtons)     
        
        samplingLayout.addLayout(mainLayout)
        samplingLayout.addLayout(reconstructionLayout)

        self.samplingTab.setLayout(samplingLayout)
    
    def freqChange(self, value):
            self.frequencyStartLabel.setText(str(value))
            self.mainPlot.resampleSingal(value)
            self.reconstractionPlot.set_data(self.mainPlot.y, self.mainPlot.x, value)

    # Composer Layout Tab
    def composerLayout(self):
        composerLayout = QVBoxLayout()
        
        # Sinusoidal Layout
        sinusoidalLayout = QHBoxLayout()
        
        panelGroupBox = QGroupBox("Sinusoidal Signal Panel")
        panelSinusoidal = QVBoxLayout()
        panelGroupBox.setLayout(panelSinusoidal)
        
        # Frequency Text Box
        self.freqBox = QLineEdit(self)
        self.freqBox.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        self.freqBox.setPlaceholderText("Frequency")

        # Magnitude Text Box
        self.magnitudeBox = QLineEdit(self)
        self.magnitudeBox.setStyleSheet(f"""font-size:14px; 
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px; 
                                background: {COLOR4};
                                color: {COLOR1};""")
        self.magnitudeBox.setPlaceholderText("Magnitude")

        # Phase Text Box
        self.phaseBox = QLineEdit(self)
        self.phaseBox.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        self.phaseBox.setPlaceholderText("Phase")

        plotButton = QPushButton("Plot")
        plotButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")

        plotButton.setIcon(QIcon("images/plot.svg"))
        plotButton.clicked.connect(self.plotSinusoidalSignal)

        panelSinusoidal.addWidget(self.freqBox)
        panelSinusoidal.addWidget(self.magnitudeBox)
        panelSinusoidal.addWidget(self.phaseBox)
        panelSinusoidal.addWidget(plotButton)
        
        # Sinusoidal Plot
        self.sinusoidalPlot = Plot()

        sinusoidalLayout.addWidget(panelGroupBox,3)
        sinusoidalLayout.addWidget(self.sinusoidalPlot,7)

        # Summition Layout
        summitionLayout = QHBoxLayout()
        
        summitionGroupBox = QGroupBox("Synthetic Signal Panel")
        summitionSinusoidal = QVBoxLayout()
        summitionGroupBox.setLayout(summitionSinusoidal)
        
        # Table of signals
        self.signalsTable = TableView()
        
        # List of signale layout
        listLayout = QHBoxLayout()
        
        # Delete of signal button 
        deleteButton = QPushButton()

        # Signals List
        self.signalsList = QComboBox()
        self.signalsList.setStyleSheet(f"""font-size:14px;
                                    height: 25px;
                                    padding: 0px 5px;
                                    background: {COLOR4};
                                    color:{COLOR1};""")
        self.signalsList.addItem("Choose...")
        
        # Delete of signal button 
        deleteButton = QPushButton()
        deleteButton.setIcon(QIcon("images/clear.svg"))
        deleteButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;""")
                            
        listLayout.addWidget(self.signalsList,4)
        listLayout.addWidget(deleteButton,1)

        confirmButton = QPushButton("Confirm")
        confirmButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")
        
        moveSamplingButton = QPushButton("Moving to Main Illustrator")
        moveSamplingButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")

        summitionSinusoidal.addWidget(self.signalsTable)
        summitionSinusoidal.addLayout(listLayout)
        summitionSinusoidal.addWidget(confirmButton)
        summitionSinusoidal.addWidget(moveSamplingButton)

        # Summition Plot  
        summitionPlot = Plot()

        summitionLayout.addWidget(summitionGroupBox, 3)
        summitionLayout.addWidget(summitionPlot ,7)

        composerLayout.addLayout(sinusoidalLayout)
        composerLayout.addLayout(summitionLayout)

        self.composerTab.setLayout(composerLayout)

    # Browse signal
    def browseSignal(self):
        path, fileExtension = QFileDialog.getOpenFileName(None, "Load Signal File", os.getenv('HOME') ,"csv(*.csv);; text(*.txt)")
        if path == "":
                return
        if fileExtension == "csv(*.csv)":
            self.mainDataPlot = pd.read_csv(path).iloc[:,0]
            self.mainDataPlot = self.mainDataPlot.values.tolist()

    def reconstructSample(self):
        if self.reconstructType.currentIndex() == 1:
            pass
        elif self.reconstructType.currentIndex() == 2:
            self.reconstractionPlot.reConstructSingal()
        else :
            self.statusBar.showMessage("Choose how you would see the reconstructed signal!")

    
    # Plot Composer Signal
    def plotSinusoidalSignal(self):
        freq = int(self.freqBox.text())
        magnitude = int(self.magnitudeBox.text())
        phase = int(self.phaseBox.text())

        signal = self.sinusoidalPlot.plotContinuousSignal(freq, magnitude, phase)
        self.signalsTable.addData(freq, magnitude, phase)
        self.signalsList.addItem("Signal " + str(self.signalsTable.rowCount()))
        self.signalSummition = np.add(self.signalSummition, signal)

    def connect(self):
        pass
    
    def hideSecGraph(self):
        if self.hidden:
            self.reconstructedframe.show()
            self.hidden = False
            self.statusBar.showMessage("The secondary graph be hidden!")
            self.hideButton.setIcon(QIcon("images/show.svg"))
        else:
            self.reconstructedframe.hide()
            self.hidden = True
            self.statusBar.showMessage("The secondary graph be unhidden!")
            self.hideButton.setIcon(QIcon("images/hide.svg"))


    def exit(self):
        exitDlg = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)

        if exitDlg == QMessageBox.Yes:
            sys.exit()
