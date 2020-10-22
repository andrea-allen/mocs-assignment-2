import numpy as np
import matplotlib.pyplot as plt
import pycxsimulator
from pylab import *
import random

def initialize():
    global grid, nextGrid
    grid = zeros([100,100])
    nextGrid = zeros([100,100])
    for i in range(100):
        for j in range(100):
            grid[i,j] = 1 if random.random() < 0.25 else 0
    grid[50, 50] = 2


def observe():
    global grid, nextGrid
    cla()
    imshow(grid, vmin=0, vmax=1, cmap=cm.summer)

def add_new_walkers():
    global grid
    for i in range(0, 5):
        for j in range(0, 5):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(95, 100):
        for j in range(0, 5):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(0, 5):
        for j in range(95, 100):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(95, 100):
        for j in range(95, 100):
            grid[i,j] = 1 if random.random() < 0.15 else 0

def update():
    global grid, nextGrid, directionGrid
    add_new_walkers()
    #For everyone that's a 1
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]==2:
                nextGrid[i][j]=2
            elif grid[i][j]==1:
                #check all neighbors
                if grid[(i-1) % 100][j % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                elif grid[(i-1) % 100][(j+1) % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                elif grid[i % 100][(j+1) % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                elif grid[(i+1) % 100][(j+1) % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                elif grid[(i+1) % 100][j % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                elif grid[(i+1) % 100][(j-1) % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                elif grid[i % 100][(j-1) % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                elif grid[(i-1) % 100][(j-1) % 100]==2:
                    nextGrid[i % 100][j % 100]=2
                else:
                    direction = generate_direction_with_attraction(i, j)
                    if direction==0:
                        nextGrid[(i-1) % 100][j % 100] = 1
                        nextGrid[i][j] = 0
                    elif direction==90:
                        nextGrid[i % 100][(j+1) % 100] = 1
                        nextGrid[i][j] = 0
                    elif direction==180:
                        nextGrid[(i+1) % 100][j % 100] = 1
                        nextGrid[i][j] = 0
                    elif direction==270:
                        nextGrid[i%100][(j-1) % 100] = 1
                        nextGrid[i % 100][j % 100] = 0
    # check NSEW etc neighbors, if anyone is a 2, you become a 2,
    # draw random direction
    # move in that direction (delete the old one)
    grid, nextGrid = nextGrid, zeros([100,100])

def generate_direction_with_attraction(i, j, attraction=True):
    #given coordinates, determine choice of direction based on the corner
    if attraction==False:
        direction = random.choice([0, 90, 180, 270])
    elif (i<=50 and j<=50):
        direction = random.choice([90, 180])
    elif (i>50 and j<=50):
        direction = random.choice([0, 90])
    elif (i<=50 and j>50):
        direction = random.choice([180, 270])
    elif (i>50 and j>50):
        direction = random.choice([0, 270])
    return direction

def sample_DLA():
    pycxsimulator.GUI().start(func=[initialize, observe, update])

if __name__ == '__main__':
    print('MOCS Assignment 2, 10-26-2020')
    sample_DLA()