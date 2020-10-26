import numpy as np
import matplotlib.pyplot as plt
import pycxsimulator
from pylab import *
import random

def initialize():
    global grid, nextGrid, gridLength
    gridLength=256
    grid = zeros([gridLength,gridLength])
    nextGrid = zeros([gridLength,gridLength])
    for i in range(gridLength):
        for j in range(gridLength):
            grid[i,j] = 1 if random.random() < 0.25 else 0
    grid[int(gridLength/2), int(gridLength/2)] = 2


def observe():
    global grid, nextGrid, finalgrid, gridLength
    cla()
    imshow(grid, vmin=0, vmax=1, cmap=cm.summer)
    finalgrid = grid

def add_new_walkers():
    global grid, gridLength
    for i in range(0, gridLength):
        for j in range(0, 1):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(0, gridLength):
        for j in range(gridLength-1, gridLength):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(0, 1):
        for j in range(0, gridLength):
            grid[i,j] = 1 if random.random() < 0.15 else 0
    for i in range(gridLength-1, gridLength):
        for j in range(0, gridLength):
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
                if grid[(i-1) % gridLength][j % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                elif grid[(i-1) % gridLength][(j+1) % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                elif grid[i % gridLength][(j+1) % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                elif grid[(i+1) % gridLength][(j+1) % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                elif grid[(i+1) % gridLength][j % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                elif grid[(i+1) % gridLength][(j-1) % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                elif grid[i % gridLength][(j-1) % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                elif grid[(i-1) % gridLength][(j-1) % gridLength]==2:
                    nextGrid[i % gridLength][j % gridLength]=2
                else:
                    direction = generate_direction_with_attraction(i, j)
                    if direction==0:
                        nextGrid[(i-1) % gridLength][j % gridLength] = 1
                        nextGrid[i][j] = 0
                    elif direction==90:
                        nextGrid[i % gridLength][(j+1) % gridLength] = 1
                        nextGrid[i][j] = 0
                    elif direction==180:
                        nextGrid[(i+1) % gridLength][j % gridLength] = 1
                        nextGrid[i][j] = 0
                    elif direction==270:
                        nextGrid[i%gridLength][(j-1) % gridLength] = 1
                        nextGrid[i % gridLength][j % gridLength] = 0
    # check NSEW etc neighbors, if anyone is a 2, you become a 2,
    # draw random direction
    # move in that direction (delete the old one)
    grid, nextGrid = nextGrid, zeros([gridLength,gridLength])

def generate_direction_with_attraction(i, j, attraction=True):
    #given coordinates, determine choice of direction based on the corner
    if attraction==False:
        direction = random.choice([0, 90, 180, 270])
    elif (i<=gridLength/2 and j<=gridLength/2):
        direction = random.choice([90, 180])
    elif (i>gridLength/2 and j<=gridLength/2):
        direction = random.choice([0, 90])
    elif (i<=gridLength/2 and j>gridLength/2):
        direction = random.choice([180, 270])
    elif (i>gridLength/2 and j>gridLength/2):
        direction = random.choice([0, 270])
    return direction

def sample_DLA():
    global finalgrid
    pycxsimulator.GUI().start(func=[initialize, observe, update])
    return finalgrid

def boxCount(grid, side_length):
    box_count_of_sidelength=0
    for i in range(0, len(grid)-side_length+1, side_length):
        for j in range(0, len(grid) - side_length+1, side_length):
            contains_cells = 0
            for k in range(i, i+side_length):
                for l in range(j, j+side_length):
                    if (grid[k][l]==2):
                        contains_cells+=1
            if contains_cells>0:
                box_count_of_sidelength+=1
    return box_count_of_sidelength


if __name__ == '__main__':
    print('MOCS Assignment 2, 10-26-2020')
    sidelengths = [128,64, 32, 16, 8, 4, 2, 1]
    final = sample_DLA()
    gridLength=256
    print("Dimension: ")
    dimension_count_array= []
    box_counts = []
    for sidelength in sidelengths:
        boxes = boxCount(final, sidelength)
        box_counts.append(boxes)
        print("Side length ", sidelength, " boxes: ", boxes)
        dimension = math.log10(boxes)/math.log10(gridLength/sidelength)
        dimension_count_array.append(dimension)
    print(dimension_count_array)
    plt.plot(np.array(sidelengths) / 256, box_counts, color='orange', lw=4, alpha=0.75, label='Number boxes needed to cover')
    plt.xlabel('Side length as fraction of total cells')
    plt.ylabel('Number boxes')
    lin_fit = (1 / (np.array(sidelengths) / 256)) ** (1.73)
    plt.plot(np.array(sidelengths) / 256, lin_fit, color='blue', lw=4, label='(1/S)^1.73')
    plt.loglog()
    plt.legend(loc='upper right')

#Side length  1  boxes:  15057
#Side length  2  boxes:  9416
#Side length  4  boxes:  3400
#Side length  8  boxes:  942
#Side length  16  boxes:  250
#Side length  32  boxes:  64
#Side length  64  boxes:  16
#Side length  128  boxes:  4