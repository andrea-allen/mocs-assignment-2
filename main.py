import numpy as np
import matplotlib.pyplot as plt
import pycxsimulator
from pylab import *
import random

def initialize():
    global grid, nextGrid, color
    global directionGrid
    color = 1
    directionGrid = initialize_random_directions(100,100)
    # directionGrid = demo2()
    grid = zeros([100,100])
    for i in range(40, 60):
        for j in range(40, 60):
            grid[i,j] = 1 if random.random() < .05 else 0
    nextGrid = zeros([100,100])

def demo2():
    #Key: North=0, NE=45, E=90, SE=135, S=180, SW=225,
    #W=270, NW=315
    #TODO How do we want to initialize the flows? This is a sample initialization for now
    directionGrid = zeros([100,100])
    for i in range(100):
        for j in range(100):
            if (i<=50 and j<=50):
                directionGrid[i][j]=90 #East
            if (i>50 and j<=50):
                directionGrid[i][j]=random.choice([135,180,225]) #Random SE, S, SW
            if (i<=50 and j>=50):
                directionGrid[i][j]=315 # NW
            if (i>50 and j>=50):
                directionGrid[i][j]=270 # West
    directionGrid = boundary_setup(directionGrid)
    return directionGrid

def boundary_setup(directionGrid):
    for i in range(len(directionGrid)):
        directionGrid[i][0] = 270
        directionGrid[0][i] = 0
        directionGrid[i][len(directionGrid)-1] = 90
        directionGrid[len(directionGrid)-1] = 180
    return directionGrid

def initialize_random_directions(n, m):
    directionGrid = zeros([n,m])
    for i in range(n):
        for j in range(m):
            directionGrid[i][j]=random.choice([0,45,90,135,180,225,270,315])
    directionGrid = boundary_setup(directionGrid)
    return directionGrid

def observe():
    global grid, nextGrid, color
    cla()
    imshow(grid, vmin=0, vmax=1, cmap=cm.nipy_spectral)
    color+=1 % 10

def update():
    global grid, nextGrid, directionGrid
    for i in range(100):
        for j in range(100):
            if grid[i][j]==0:
                continue
            elif grid[i][j]==1:
                nextGrid[i][j]=1
                try:
                    if directionGrid[i][j]==0: #North
                        nextGrid[i-1][j]=1
                    if directionGrid[i][j]==45: #NE
                        nextGrid[i-1][j]=1
                        nextGrid[i][j+1]=1
                        nextGrid[i-1][j+1]=1
                    if directionGrid[i][j]==90: #East
                        nextGrid[i][j+1]=1
                    if directionGrid[i][j]==135: #SE
                        nextGrid[i][j+1] = 1
                        nextGrid[i+1][j] = 1
                        nextGrid[i+1][j + 1] = 1
                    if directionGrid[i][j]==180: #South
                        nextGrid[i+1][j]=1
                    if directionGrid[i][j]==225: #SW
                        nextGrid[i+1][j] = 1
                        nextGrid[i][j-1] = 1
                        nextGrid[i+1][j-1] = 1
                    if directionGrid[i][j]==270: #West
                        nextGrid[i][j-1]=1
                    if directionGrid[i][j]==315: #NW
                        nextGrid[i][j-1] = 1
                        nextGrid[i-1][j] = 1
                        nextGrid[i-1][j-1] = 1
                except IndexError:
                    continue
    grid, nextGrid = nextGrid, grid

def sample_CA():
    pycxsimulator.GUI().start(func=[initialize, observe, update])

if __name__ == '__main__':
    print('MOCS Assignment 2, 10-26-2020')
    sample_CA()


