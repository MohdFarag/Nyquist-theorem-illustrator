# importing Qt widgets
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
        if analog_time[0] != 0:
            time_interval = analog_time[-1] - analog_time[0]
        else :
            time_interval = analog_time[-1]
        nsamples = int(np.ceil(sampling_freq * time_interval))

        if analog_time[0] == 0:
            time_interval *= 2

        if nsamples > 0:
            sampling_time = np.arange(min(analog_time), time_interval/2, 1/sampling_freq)
            sampling_values = [originalSignal[np.searchsorted(analog_time, t)] for t in sampling_time]
            return (sampling_time, sampling_values)
        # return null list if there is no samples
        return ([0], [0])


    def sampleSingal(self, newSample):
        self.clearSignal()

        # Update new sampling rate
        self.sampling = newSample
        self.sampledTime, self.sampledSignal = self.sample(self.y, self.sampling, self.x) # Sample data
                
        # Plot Original Signal
        self.axes.plot(self.x, self.y)
        
        # Plot Sampled Signal
        self.axes.plot(self.sampledTime, self.sampledSignal, '.', self.sampling)
        
        # Plot Sampled Signal dashed
        resampledSignal = self.sincInterpolation(self.sampledSignal, self.sampledTime) # Sinc interpolation

        # Plot dashed line
        self.axes.plot(self.x, resampledSignal, 'r--', self.sampling)

        self.draw()

        return self.sampledTime, self.sampledSignal

    def sincInterpolation(self, sampledSignal, sampledTime):
        inputTime = np.array(sampledTime)
        inputMag = np.array(sampledSignal)

        period = inputTime[1] - inputTime[0]
        
        sincM = np.tile(self.x, (len(inputTime), 1)) - np.tile(inputTime[:, np.newaxis], (1, len(self.x)))
        outputMag = np.dot(inputMag, np.sinc(sincM / period))
        
        return outputMag

    def resampleSignalLine(self):
        # Clear signal
        self.clearSignal()

        # Generate resample signal        
        resampledSignal = self.sincInterpolation(self.sampledSignal, self.sampledTime)

        # Plot resample signal 
        self.axes.plot(self.x, resampledSignal, '-', self.sampling)

        self.draw()

    def clearSignal(self):
        self.axes.clear()
        self.axes.set_xlim([min(self.x), max(self.x)])
        self.axes.set_ylim([min(self.y), max(self.y)+1])