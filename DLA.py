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
    global grid, nextGrid, finalgrid
    cla()
    imshow(grid, vmin=0, vmax=1, cmap=cm.summer)
    finalgrid = grid

def add_new_walkers():
    global grid
    for i in range(0, 100):
        for j in range(0, 1):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(0, 100):
        for j in range(99, 100):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(0, 1):
        for j in range(0, 100):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(99, 100):
        for j in range(0, 100):
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
    global finalgrid
    pycxsimulator.GUI().start(func=[initialize, observe, update])
    return finalgrid

def boxCount(grid):
    # global finalgrid
    box_count_full=0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]==2:
                box_count_full+=1
    return box_count_full


if __name__ == '__main__':
    print('MOCS Assignment 2, 10-26-2020')
    final = sample_DLA()
    print(final)
    print(final[50])
    number = boxCount(final)
    print("Box count ", number)
    print("Dimension: ")
    dimension = math.log10(number)/math.log10(100)
    print(dimension)