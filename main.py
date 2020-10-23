import numpy as np
import matplotlib.pyplot as plt
import pycxsimulator
from pylab import *
import random

def initialize():
    global grid, nextGrid
    global directionGrid
    # directionGrid = initialize_random_directions(100,100)
    directionGrid = interesting_flow()
    grid = zeros([100,100])
    for i in range(0, 10):
        for j in range(0, 10):
            grid[i,j] = 1 if random.random() < .75 else 0
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

def interesting_flow():
    directionGrid = zeros([100,100])
    for i in range(100):
        for j in range(100):
            if (i>=0 and i < 25):
                if (j>=0 and j<25):
                    directionGrid[i][j] = random.choice([90, 135, 180])
                elif (j>=25 and j<50):
                    directionGrid[i][j] = random.choice([90])
                elif (j>=50 and j<75):
                    directionGrid[i][j] = random.choice([90, 180])
                elif (j>=75 and j<100):
                    directionGrid[i][j] = random.choice([0,45,90,135,180,225,270,315])
            if (i>=25 and i<50):
                if (j>=0 and j<25):
                    directionGrid[i][j] = random.choice([90, 135, 180])
                elif (j>=25 and j<50):
                    directionGrid[i][j] = random.choice([180, 135])
                elif (j>=50 and j<75):
                    directionGrid[i][j] = random.choice([180, 135])
                elif (j>=75 and j<100):
                    directionGrid[i][j] = random.choice([180, 135])
            if (i>=50 and i<75):
                if (j>=0 and j<25):
                    directionGrid[i][j] = random.choice([180, 225])
                elif (j>=25 and j<50):
                    directionGrid[i][j] = random.choice([270, 225])
                elif (j>=50 and j<75):
                    directionGrid[i][j] = random.choice([135, 90])
                elif (j>=75 and j<100):
                    directionGrid[i][j] = random.choice([180, 135, 90])
            if (i>=75 and i<100):
                if (j>=0 and j<25):
                    directionGrid[i][j] = random.choice([180, 270, 225])
                elif (j>=25 and j<50):
                    directionGrid[i][j] = random.choice([180, 270, 225])
                elif (j>=50 and j<75):
                    directionGrid[i][j] = random.choice([180, 135])
                elif (j>=75 and j<100):
                    directionGrid[i][j] = random.choice([180, 225, 135])
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
    global grid, nextGrid
    cla()
    imshow(grid, vmin=0, vmax=1, cmap=cm.nipy_spectral)

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


