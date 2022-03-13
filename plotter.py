# !/usr/bin/python

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
    def __init__(self,title="Signal Plot"):
        
        """Initializer."""
        super().__init__()
        self.plot = self.addPlot()

        self.plot.setTitle(title, size="20pt")
        self.plot.setLabel('bottom', 'Time', 's')
        self.plot.showGrid(x=True, y=True)

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