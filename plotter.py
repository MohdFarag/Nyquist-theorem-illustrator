# !/usr/bin/python

# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Definition of Main Color Palette
from Defs import COLOR1, COLOR2, COLOR3, COLOR4, COLOR5

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
        self.setStyleSheet(f"border-radius: 6px;")

        self.plot = self.addPlot()

        self.plot.setTitle(title, size = "20pt")
        self.plot.setLabel('bottom', 'Time', 's')
        #self.plot.showGrid(x=True, y=True)
        
        self.setBackground(f'{COLOR1}')
        self.plot.getAxis('left').setPen(f"{COLOR4}")
        self.plot.getAxis('bottom').setPen(f"{COLOR4}")

        self.y = [0]
        self.x = [0]

    def plotSignal(self, x, y):
        self.clearPlot()
        self.plot.plot(x,y)

    def clearPlot(self):
        self.plot.clear()