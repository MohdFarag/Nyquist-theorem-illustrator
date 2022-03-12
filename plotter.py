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

class Plot(pg):
    """Main Plot."""
    def __init__(self):
        
        """Initializer."""
        super().__init__()