# importing Qt widgets
FACTOR = 1.1
from turtle import color
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from scipy import signal
from scipy.special import sinc


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
        self.sampledTime, self.sampledSignal = [],[]
        
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


    def set_data(self, y, x, sampling=1 ,sampledTime=[], sampledSignal=[]):
        self.y = y
        self.x = x
        
        self.sampledTime = sampledTime 
        self.sampledSignal = sampledSignal
        self.sampling = sampling

    def plotSignal(self):
        self.clearSignal()
        self.axes.plot(self.x, self.y)
        self.draw()

    def sample(self, originalSignal, sampling_freq, analog_time):
        time_interval = analog_time[-1]
        nsamples = int(np.ceil(sampling_freq * time_interval))
        if nsamples > 0:
            sampling_time = np.arange(min(analog_time), time_interval, 1/sampling_freq)
            sampling_values = [originalSignal[np.searchsorted(analog_time, t)] for t in sampling_time]
            return (sampling_time, sampling_values)
        # return null list if there is no samples
        return ([0], [0])


    def sampleSingal(self, newSample):
        self.sampling = newSample
        self.clearSignal()
        
        self.sampledTime, self.sampledSignal = self.sample(self.y, FACTOR*self.sampling, self.x)
                
        # Plot Original Signal
        self.axes.plot(self.x, self.y)
        
        # Plot Sampled Signal
        self.axes.plot(self.sampledTime, self.sampledSignal, '.', self.sampling)
        
        # Plot Sampled Signal dashed
        resampledSignal, resampledTime = signal.resample(self.sampledSignal, len(self.y), self.sampledTime)
        
        # Plot dashed line
        self.axes.plot(resampledTime, resampledSignal, 'r--', self.sampling)

        self.draw()

        return self.sampledTime, self.sampledSignal
    
    def resampleSignalLine(self):
        self.clearSignal()

        # Generate resample signal        
        resampledSignal, resampledTime = signal.resample(self.sampledSignal, len(self.y), self.sampledTime)
        
        # Plot resample signal 
        self.axes.plot(resampledTime, resampledSignal, '-', self.sampling)

        self.draw()

    def clearSignal(self):
        self.axes.clear()
        self.axes.set_xlim([min(self.x), max(self.x)])
        self.axes.set_ylim([min(self.y), max(self.y)+1])