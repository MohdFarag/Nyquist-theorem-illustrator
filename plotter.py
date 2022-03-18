# !/usr/bin/python

# Definition of Main Color Palette
global COLOR1, COLOR2, COLOR3, COLOR4
COLOR1 = "#222831"
COLOR2 = "#393E46"
COLOR3 = "#00ADB5"
COLOR4 = "#EEEEEE"

# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# importing numpy and pandas
import numpy as np
import pandas as pd

# importing pyqtgraph as pg
import pyqtgraph as pg

class Plot(pg.GraphicsLayoutWidget):
    """Main Plot."""
    def __init__(self,title=""):
        
        """Initializer."""
        super().__init__()
        self.plot = self.addPlot()

        self.plot.setTitle(title, size="20pt")
        self.plot.setLabel('bottom', 'Time', 's')
        self.plot.showGrid(x=True, y=True)
        
        self.setBackground(f'{COLOR1}')
        self.plot.getAxis('left').setPen(f"{COLOR4}")
        self.plot.getAxis('bottom').setPen(f"{COLOR4}")


    def plotContinuousSignal(self, frequency, magnitude, phase):
        tMin = -np.pi/2
        tMax = np.pi/2
        t = np.linspace(tMin, tMax, 1000)
        y = magnitude * np.sin(2 * np.pi * frequency * t + phase)
        self.plot.plot(t, y)
        
        return(y)

    def plotDiscreteSignal(self, y, x=np.linspace(-5, 5, 1000)):
        self.plot.plot(x, y)

    def clearPlot(self):
        self.plot.clear()