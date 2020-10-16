import numpy as np
import matplotlib.pyplot as plt
import pycxsimulator
from pylab import *

def initialize():
    global grid, nextGrid
    grid = zeros([100,100])
    grid[10, 15] = 1
    grid[22, 35] = 1
    nextGrid = zeros([100,100])

def observe():
    global grid, nextGrid
    cla()
    imshow(grid, vmin=0, vmax=1, cmap = cm.binary)

def update():
    global grid, nextGrid
    grid, nextGrid = nextGrid, grid

def sample_CA():
    pycxsimulator.GUI().start(func=[initialize, observe, update])

if __name__ == '__main__':
    print('MOCS Assignment 2, 10-26-2020')
    sample_CA()


