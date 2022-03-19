# importing Qt widgets
from turtle import color
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from scipy import signal

# Definition of Main Color Palette
from Defs import COLOR1, COLOR2, COLOR3, COLOR4, COLOR5

# importing numpy and pandas
import numpy as np
import pandas as pd

# matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from random import randint

class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None,title="Signal Plot"):
        
        self.y = [0]
        self.x = np.linspace(-np.pi/2, np.pi/2, 1000)
        self.sampling = 1
        
        self.fig = Figure(facecolor=f"{COLOR1}")

        self.axes = self.fig.add_subplot(111)
                
        self.axes.set_title(title, fontweight ="bold", color=f"{COLOR4}")
        self.axes.set_xlabel("Time", color=f"{COLOR4}")
        self.axes.set_ylabel("Amplitude", color=f"{COLOR4}")
        self.axes.set_facecolor(f"{COLOR1}")
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)

        self.axes.spines['bottom'].set_color(f"{COLOR4}")
        self.axes.spines['left'].set_color(f"{COLOR4}")

        self.axes.tick_params(axis='x', colors=f"{COLOR4}")
        self.axes.tick_params(axis='y', colors=f"{COLOR4}")
        
        super(MplCanvas, self).__init__(self.fig)


    def set_data(self, y, x, sampling=1):
        self.y = y
        self.x = x
        self.sampling = sampling

    def plotContinuousSignal(self, frequency, magnitude, phase):
        self.clearSignal()

        tMin = -np.pi/2
        tMax = np.pi/2
        self.t = np.linspace(tMin, tMax, 1000)
        self.y = magnitude * np.sin(2 * np.pi * frequency * self.x + phase)
        self.axes.plot(self.x, self.y)

    def plotDiscreteSignal(self):
        self.clearSignal()

        self.axes.plot(self.x, self.y)

        self.draw()

    def resampleSingal(self, newSample):
        self.sampling = newSample

        self.clearSignal()
        
        f = signal.resample(self.y, newSample)
        xNew = np.linspace(-np.pi/2, np.pi/2, newSample)
        
        # Plot Original Signal
        self.axes.plot(self.x, self.y)
        # Plot Sampled Signal
        self.axes.plot(xNew, f, '.', newSample)

        self.draw()

    def reConstructSingal(self):     
        self.clearSignal()
        
        f = signal.resample(self.y, self.sampling)
        xNew = np.linspace(-np.pi/2, np.pi/2, self.sampling)
        
        # Plot Sampled Signal
        self.axes.plot(xNew, f, '-', self.sampling)

        self.draw()
        
    def clearSignal(self):
        self.axes.clear()
        self.axes.set_xlim([min(self.x), max(self.x)])
        self.axes.set_ylim([min(self.y), max(self.y)])