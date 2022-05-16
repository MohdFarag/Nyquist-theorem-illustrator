# !/usr/bin/python

# import Plotter.py Class
import ast
from cmath import nan
from math import floor
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
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['Frequency','Magnitude','Phase'])
 
    def addData(self, frequency, magnitude, phase): 
        rowPosition = self.rowCount()

        self.insertRow(rowPosition)
        self.setItem(rowPosition , 0, QTableWidgetItem(f"{frequency}Hz"))
        self.setItem(rowPosition , 1, QTableWidgetItem(f"{magnitude}"))
        self.setItem(rowPosition , 2, QTableWidgetItem(f"{phase}°"))

    def clearAllData(self):
        self.setRowCount(0)
        
class Window(QMainWindow):
    """Main Window."""
    def __init__(self):
        
        """Initializer."""
        super().__init__()

        # Initialize Variables
        self.mainDataPlot = []
        self.timePlot = []
        self.signalSummition = [0 for _ in range(0,1000)]
        self.hidden = False
        self.maxFreq = 0

        # setting Icon
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

        self.connect()

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

        # Main Buttons Layout
        mainButtons = QHBoxLayout()

        # Sampling slider
        self.frequencyStartLabel = QLabel("1")
        self.frequencyStartLabel.setStyleSheet("font-size: 13px;padding: 2px;font-weight: 800;")

        self.sliderMainPlot = QSlider(Qt.Horizontal,self)
        self.sliderMainPlot.setMinimum(1)
        self.sliderMainPlot.setMouseTracking(False)
        self.sliderMainPlot.setSingleStep(50)
        self.sliderMainPlot.setMaximum(300)

        self.frequencyEndLabel = QLabel(u'3 F\u2098\u2090\u2093')
        
        self.frequencyEndLabel.setStyleSheet("font-size: 13px;padding: 2px;font-weight: 800;")
        
        # Reconstruct signal type : dotted or secondary graph
        self.reconstructType = QComboBox()
        self.reconstructType.setStyleSheet(f"""font-size:14px;
                                    height: 25px;
                                    padding: 0px 5px;
                                    background: {COLOR4};
                                    color:{COLOR1};""")
        self.reconstructType.addItem("Choose")
        self.reconstructType.addItem("Dotted signal")
        self.reconstructType.addItem("In Secondary graph")

        # Sampling Buttons
        self.plotReconstructButton = QPushButton("Reconstruct")
        self.plotReconstructButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")
 
        mainButtons.addWidget(self.frequencyStartLabel)
        mainButtons.addWidget(self.sliderMainPlot)
        mainButtons.addWidget(self.frequencyEndLabel)
        #mainButtons.addWidget(self.reconstructType)
        mainButtons.addWidget(self.plotReconstructButton)

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

        reconstructButtons.addWidget(self.hideButton)
        reconstructButtons.addSpacerItem((QSpacerItem(30, 10, QSizePolicy.Expanding)))
        
        reconstructionLayout.addWidget(self.reconstructedframe)
        reconstructionLayout.addLayout(reconstructButtons)     
        
        samplingLayout.addLayout(mainLayout)
        samplingLayout.addLayout(reconstructionLayout)

        self.samplingTab.setLayout(samplingLayout)
    
    # Frequency change
    def freqChange(self, value):
            sampling_freq = float(value)/100 * float(self.maxFreq)

            # Update values of labels of slider
            self.frequencyStartLabel.setText(str(round(sampling_freq, 1)) + " Hz")
            text = str(value/100) + u'F\u2098\u2090\u2093'
            self.frequencyEndLabel.setText(text)

            # Sample signal
            sampledTime, sampledSignal = self.mainPlot.sampleSingal(sampling_freq)

            # Update Data in reconstructed Plot
            self.reconstractionPlot.set_data(self.mainPlot.y, self.mainPlot.x, sampling_freq, sampledTime, sampledSignal)

    # Composer Layout Tab
    def composerLayout(self):
        composerLayout = QVBoxLayout()
        
        # Sinusoidal Layout
        sinusoidalLayout = QHBoxLayout()
        
        panelGroupBox = QGroupBox("Sinusoidal Signal Panel")
        panelSinusoidal = QVBoxLayout()
        panelGroupBox.setLayout(panelSinusoidal)
        
        # Frequency Text Box
        self.freqBox = QSpinBox(self)
        self.freqBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        self.freqBox.setValue(int(1))
        # Magnitude Text Box
        self.magnitudeBox = QSpinBox(self)
        self.magnitudeBox.setStyleSheet(f"""font-size:14px; 
                                padding: 5px 15px; 
                                background: {COLOR4};
                                color: {COLOR1};""")
        self.magnitudeBox.setValue(int(1))
        # Phase Text Box
        self.phaseBox = QSpinBox(self)
        self.phaseBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        self.phaseBox.setValue(int(0))

        self.plotButton = QPushButton("Plot | Add")
        self.plotButton.setStyleSheet(f"""font-size:14px; 
                            border-radius: 6px;
                            border: 1px solid {COLOR1};
                            padding: 5px 15px; 
                            background: {COLOR1}; 
                            color: {COLOR4};""")

        self.plotButton.setIcon(QIcon("images/plot.svg"))

        panelSinusoidal.addWidget(QLabel("Frequency:"))
        panelSinusoidal.addWidget(self.freqBox)
        panelSinusoidal.addWidget(QLabel("Magnitude:"))
        panelSinusoidal.addWidget(self.magnitudeBox)
        panelSinusoidal.addWidget(QLabel("Phase:"))
        panelSinusoidal.addWidget(self.phaseBox)
        panelSinusoidal.addWidget(self.plotButton)
        
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
        
        # Signals List
        self.signalsList = QComboBox()
        self.signalsList.setStyleSheet(f"""font-size:14px;
                                    height: 25px;
                                    padding: 0px 5px;
                                    background: {COLOR4};
                                    color:{COLOR1};""")
        self.signalsList.addItem("Choose...")
        
        # Delete of signal button 
        self.deleteButton = QPushButton()
        self.deleteButton.setIcon(QIcon("images/clear.svg"))
        self.deleteButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;""")

        listLayout.addWidget(self.signalsList,4)
        listLayout.addWidget(self.deleteButton,1)
        
        self.saveExampleButton = QPushButton("Save")
        self.saveExampleButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")

        self.confirmButton = QPushButton("Mix | Plot")
        self.confirmButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")
        
        saveAndConfLayout = QHBoxLayout()
        saveAndConfLayout.addWidget(self.saveExampleButton,2)
        saveAndConfLayout.addWidget(self.confirmButton,2)

        self.moveSamplingButton = QPushButton("Moving to Main Illustrator")
        self.moveSamplingButton.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")

        summitionSinusoidal.addWidget(self.signalsTable)
        summitionSinusoidal.addLayout(listLayout)
        summitionSinusoidal.addLayout(saveAndConfLayout)
        summitionSinusoidal.addWidget(self.moveSamplingButton)

        # Summition Plot  
        self.summitionPlot = Plot()

        summitionLayout.addWidget(summitionGroupBox, 3)
        summitionLayout.addWidget(self.summitionPlot ,7)

        exampleGroupBox = QGroupBox("Saved Examples")
        exampleLayout = QHBoxLayout()
        exampleGroupBox.setLayout(exampleLayout)

        self.examplesList = QComboBox()
        self.examplesList.setStyleSheet(f"""font-size:14px;
                                    height: 25px;
                                    padding: 0px 5px;
                                    background: {COLOR4};
                                    color:{COLOR1};""")
        self.examplesList.addItem("Choose...")
        # Read Data of examples
        self.bigExamplesList = self.readExamples()

        self.preview = QPushButton("Preview")
        self.preview.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")

        self.export = QPushButton("Export")
        self.export.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;
                                color:{COLOR4}""")
        
        self.deleteEx = QPushButton("")
        self.deleteEx.setIcon(QIcon("images/clear.svg"))
        self.deleteEx.setStyleSheet(f"""background: {COLOR1};
                                border-radius: 6px;
                                border: 1px solid {COLOR1};
                                padding: 5px 15px;""")


        exampleLayout.addWidget(self.examplesList, 10)
        exampleLayout.addWidget(self.preview, 4)
        exampleLayout.addWidget(self.export, 4)
        exampleLayout.addWidget(self.deleteEx, 1)

        composerLayout.addLayout(sinusoidalLayout)
        composerLayout.addLayout(summitionLayout)
        composerLayout.addWidget(exampleGroupBox)

        self.composerTab.setLayout(composerLayout)

    # Browse signal
    def browseSignal(self):
        path, fileExtension = QFileDialog.getOpenFileName(None, "Load Signal File", os.getenv('HOME') ,"csv(*.csv)")
        if path == "":
                return
                
        if fileExtension == "csv(*.csv)":
            self.mainDataPlot = pd.read_csv(path).iloc[:,1].values.tolist()
            self.timePlot = pd.read_csv(path).iloc[:,0].values.tolist()

        self.maxFreq = self.getFmax() # Get Frequency Maximum

        self.mainPlot.clearSignal()
        self.mainPlot.set_data(self.mainDataPlot, self.timePlot)
        self.mainPlot.plotSignal()

    def getFmax(self):
        # gets array of fft magnitudes
        fft_magnitudes = np.abs(np.fft.fft(self.mainDataPlot))
        # gets array of frequencies
        fft_frequencies = np.fft.fftfreq(len(self.timePlot), self.timePlot[2]-self.timePlot[1])
        # create new "clean array" of frequencies
        fft_clean_frequencies_array = []
        for index in range(len(fft_frequencies)):
            # checks if signigifcant frequency is present
            if fft_magnitudes[index] > np.average(fft_magnitudes):
                fft_clean_frequencies_array.append(fft_frequencies[index])

        maxFreq = floor(max(fft_clean_frequencies_array))

        return maxFreq

    def reconstructSample(self):
        self.reconstractionPlot.resampleSignalLine()

    # Plot Composer Signal
    def plotSinusoidalSignal(self):
        freq = float(self.freqBox.text())
        magnitude = float(self.magnitudeBox.text())
        phase = float(self.phaseBox.text())

        signal, t = self.getContinuosSignal(freq, magnitude, phase)

        self.sinusoidalPlot.plotSignal(t, signal)
        self.signalsTable.addData(freq, magnitude, phase)
        self.signalsList.addItem("Signal " + str(self.signalsTable.rowCount()))

    # Signal Summution
    def signalSummitionPlot(self):
        self.signalSummition = [0 for _ in range(0,1000)]

        i = 0
        while i < self.signalsTable.rowCount() :
            frequency = self.signalsTable.item(i,0).data(0)[:-2]
            magnitude = self.signalsTable.item(i,1).data(0)
            phase = self.signalsTable.item(i,2).data(0)[:-1]
            
            y, _ = self.getContinuosSignal(frequency, magnitude, phase)
            i+=1
            
            self.signalSummition = np.add(self.signalSummition,y)

        self.summitionPlot.clearPlot()
        self.summitionPlot.plotSignal(np.linspace(-2*np.pi, 2*np.pi, 1000), self.signalSummition)

    # Delete signal from the list
    def deleteSignal(self):
        if self.signalsList.currentText() != "Choose...":
            currentIndex = int(self.signalsList.currentIndex()) - 1

            self.signalsTable.removeRow(int(self.signalsList.currentText()[7])-1)        
            self.signalsList.removeItem(self.signalsList.currentIndex())

            while currentIndex < self.signalsList.count():
                currentIndex += 1
                self.signalsList.setItemText(currentIndex,"Signal " + str(currentIndex))

    # Hide secondary Plot        
    def hideSecGraph(self):
        if self.hidden:
            self.reconstructedframe.show()
            self.hidden = False
            self.statusBar.showMessage("The secondary graph be unhidden!")
            self.hideButton.setIcon(QIcon("images/show.svg"))
        else:
            self.reconstructedframe.hide()
            self.hidden = True
            self.statusBar.showMessage("The secondary graph be hidden!")
            self.hideButton.setIcon(QIcon("images/hide.svg"))

    # Return continuos signal given frequency, magnitude and phase: A cos(2*pi*freq*t + phase) 
    def getContinuosSignal(self, frequency, magnitude, phase):
        tMin = -2*np.pi
        tMax = 2*np.pi

        t = np.linspace(tMin, tMax, 1000)
        y = float(magnitude) * np.sin(2 * np.pi * float(frequency) * t + float(phase))

        return (y, t)

    def moveToSamplePlot(self):
        freqList = list()
        i = 0
        # Get Fmax
        while i < self.signalsTable.rowCount() :
            frequency = self.signalsTable.item(i,0).data(0)[:-2]
            freqList.append(float(frequency))
            i+=1
        self.maxFreq = max(freqList)
        self.mainPlot.clearSignal()
        self.mainPlot.set_data(self.signalSummition, np.linspace(-2*np.pi, 2*np.pi, 1000))
        self.mainPlot.plotSignal()
    
    def connect(self):
        self.sliderMainPlot.valueChanged[int].connect(self.freqChange)
        self.hideButton.clicked.connect(self.hideSecGraph)

        self.deleteButton.clicked.connect(self.deleteSignal)
        self.saveExampleButton.clicked.connect(self.AddExample)
        self.confirmButton.clicked.connect(self.signalSummitionPlot)
        self.moveSamplingButton.clicked.connect(self.moveToSamplePlot)
        
        self.plotButton.clicked.connect(self.plotSinusoidalSignal)
        self.plotReconstructButton.clicked.connect(self.reconstructSample)

        self.preview.clicked.connect(self.loadExample)
        self.export.clicked.connect(self.exportExample)
        self.deleteEx.clicked.connect(self.deleteExample)

    ### Examples Functions

    def deleteExample(self):
        currentIndex = int(self.examplesList.currentIndex()) - 1

        self.bigExamplesList.pop(int(self.examplesList.currentText()[-1])-1)
        self.examplesList.removeItem(self.examplesList.currentIndex())

        while currentIndex < self.examplesList.count():
            currentIndex +=1
            self.examplesList.setItemText(currentIndex,"Example " + str(currentIndex))
        
        df = pd.DataFrame(self.bigExamplesList)
        df.to_csv('ExamplesList.csv')
        
    def exportExample(self):
        exampleIndex = int(self.examplesList.currentText()[-1]) - 1 # compoBox Begin from 1
        exampleInfo = self.bigExamplesList[exampleIndex]
        
        t = np.linspace(-2*np.pi, 2*np.pi, 1000)
        signal = 0 * t

        for signalInfo in exampleInfo:
            freq = signalInfo[0]
            magnitude = signalInfo[1]
            phase = signalInfo[2]

            partSignal, _ = self.getContinuosSignal(freq, magnitude, phase)
            signal += partSignal
        
        dict = {'time': t, 'magnitude': signal}  
        df = pd.DataFrame(dict)
        output_file, _ = QFileDialog.getSaveFileName(self, 'Export File', None, 'CSV files (.csv);;All Files()')
        if output_file != '':
            if QFileInfo(output_file).suffix() == "" : output_file += '.csv'

        df.to_csv(output_file, index=False)
    
    # Transfer list to string
    def stringToList(self, stringList):
        List = ast.literal_eval(stringList)
        try:
            List = [n.strip() for n in List]
        except:
            pass
        List = [float(n) for n in List]

        return List

    # Read Examples from csv file 
    def readExamples(self):        
            listExamples = list()
            df = pd.read_csv("ExamplesList.csv")
            for i in range(df.shape[0]):
                listExample = list()
                for j in range(1, df.shape[1]):
                    signalData = (df.iloc[i,j])
                    if not pd.isna(signalData):
                        signalData = self.stringToList(signalData)
                        listExample.append(signalData)
                listExamples.append(listExample)
            
            for _ in listExamples: 
                self.examplesList.addItem("Example " + str(self.examplesList.count()))

            return listExamples        
        # except:
        #     QMessageBox.warning(self, "Error", "Error in open file.")
        #     return []
    
    # Preview loaded example 
    def loadExample(self):
        exampleIndex = int(self.examplesList.currentText()[-1]) - 1 # compoBox Begin from 1
        exampleInfo = self.bigExamplesList[exampleIndex]

        self.signalsTable.clearAllData()
        self.signalsList.clear()

        self.signalsList.addItem("Choose...")
        self.previewExample(exampleInfo)

    def AddExample(self):
        signalSum = []
        i = 0
        while i < self.signalsTable.rowCount() :
            frequency = self.signalsTable.item(i,0).data(0)[:-2]
            magnitude = self.signalsTable.item(i,1).data(0)
            phase = self.signalsTable.item(i,2).data(0)[:-1]
            
            signalInfo = [frequency, magnitude, phase]
            signalSum.append(signalInfo)      
            i+=1
         
        self.bigExamplesList.append(signalSum)
        self.examplesList.addItem("Example " + str(self.examplesList.count()))

        df = pd.DataFrame(self.bigExamplesList)
        
        try:
            df.to_csv('ExamplesList.csv')
        except:
            QMessageBox.critical(self, "Error", "There is a problem, be sure that the examples.csv is closed.")

    def previewExample(self, exampleInfo) :
        for signalInfo in exampleInfo:
            freq = signalInfo[0]
            magnitude = signalInfo[1]
            phase = signalInfo[2]

            self.signalsTable.addData(freq, magnitude, phase)
            self.signalsList.addItem("Signal " + str(self.signalsTable.rowCount()))

            self.signalSummitionPlot()

    def exit(self):
        exitDlg = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)

        if exitDlg == QMessageBox.Yes:
            sys.exit()
