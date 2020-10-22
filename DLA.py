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

def boxCount(grid, gridLength, side_length):
    box_count_full=0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]==2:
                box_count_full+=1
    box_count_sidelength=0
    for i in range(0, len(grid)-side_length+1, side_length):
        for j in range(0, len(grid) - side_length+1, side_length):
            contains_cells = False
            for k in range(i, i+side_length):
                for l in range(j, j+side_length):
                    contains_cells=(grid[k][l]==2)
            if contains_cells:
                box_count_sidelength+=1
    return box_count_sidelength


if __name__ == '__main__':
    print('MOCS Assignment 2, 10-26-2020')
    final = sample_DLA()
    print(final)
    print(final[50])
    # number = boxCount(final, 100, 50)
    gridLength=256
    # print("Box count ", number)
    print("Dimension: ")
    dimension_count_array= []
    for sidelength in [1,2,4,8,16,32,64,128]:
        boxes = boxCount(final, gridLength, sidelength)
        print("Side length ", sidelength, " boxes: ", boxes)
        dimension = math.log10(boxes)/math.log10(gridLength/sidelength)
        dimension_count_array.append(dimension)
    print(dimension_count_array)
    plt.plot(np.array(dimension_count_array))
    plt.show()