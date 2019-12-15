import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
from Day9 import IntCode
from random import random;
    

            
def print_grid(grid, pos):
    fig = plt.figure(1);
    ax = fig.add_subplot(1,1,1);
    colors = 'krg'
    for col in range(-1,2):
        xs = []
        ys = []
        for coord in grid:
            if grid[coord] == col:
                xs.append(coord[0]);
                ys.append(coord[1]);
        ax.scatter(xs, ys, color=colors[col+1]);
    ax.scatter(pos[0], pos[1], color='b')

def checkDir(grid, pos, intcode):
    move_dirs = {1 : np.array([0,1]), 2 : np.array([0,-1]), 3 : np.array([-1,0]), 4 : np.array([1,0])}
    backwards = {1 : 2, 2 : 1, 3 : 4, 4 : 3};
    moveable = []
    for j in range(1,5):
        target_pos = tuple(pos + move_dirs[j]);
        if target_pos in grid:
            if grid[target_pos] == 0 or grid[target_pos] == -1:
                continue;
        intcode.execute(j, True);
        grid[target_pos] = intcode.outputs[0];
        if intcode.outputs[0] == 1:
            nzeros = 0;
            for k in range(1,5):
                if k != backwards[j]:
                    if tuple(pos + move_dirs[j] + move_dirs[k]) in grid:
                        if grid[tuple(pos + move_dirs[j] + move_dirs[k])] == 0 or grid[tuple(pos + move_dirs[j] + move_dirs[k])] == -1:
                            nzeros += 1;
                        else:
                            break;
                    else:
                        break;
            if nzeros == 3:
                grid[target_pos] = -1;
            else:
                moveable.append(j);
            intcode.execute(backwards[j], True);
        if intcode.outputs[0] == 2:
            intcode.execute(backwards[j], True);
            moveable = [j];
            break;
    return moveable;
        
        
        
    
    

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day15.txt', header=None).T;
    data.columns=['opcode']
    intcode = IntCode(data.values.T[0]);
    
    move_dirs = {1 : np.array([0,1]), 2 : np.array([0,-1]), 3 : np.array([-1,0]), 4 : np.array([1,0])}

    
    steps = {(0,0) : 0}
    grid = {(0,0) : 1}
    pos = np.array([0,0])
    #%%
    i = 0;
    while i < 1500:
        # move_dir = (random()*4)//1 + 1
        # intcode.execute(move_dir, True);
        moveable = checkDir(grid, pos, intcode)
        if len(moveable) == 1:
            grid[tuple(pos)] = -1;
            intcode.execute(moveable[0], True);
            move = moveable[0];
        else:
            foundmove = False;
            for di in moveable:
                hasunknown = False;
                for k in range(1,5):
                    if tuple(pos + move_dirs[di] + move_dirs[k]) not in grid:
                        hasunknown = True;
                        break;
                if hasunknown:
                    foundmove = True;
                    intcode.execute(di, True);
                    move = di;
                    break;
            if not foundmove:
                move_dir = int(random()*len(moveable));
                intcode.execute(moveable[move_dir], True);
                move = moveable[move_dir];
        pos += move_dirs[move];
        adjacentlocations = []
        for k in range(1,5):
            if tuple(pos + move_dirs[k]) in steps:
                adjacentlocations.append(steps[tuple(pos + move_dirs[k])]);
        steps[tuple(pos)] = min(adjacentlocations) + 1;
        if intcode.outputs[0] == 2:
            print('found');
            break;
        i += 1;
    print_grid(grid, pos);
    
            
    print("Day 15-1 answer is {0}".format(steps[tuple(pos)]));
    t1= time.time();
    
    intcode.execute(4, True);
    intcode.execute(4, True);
    grid = {tuple(pos) : 0, tuple(pos+np.array([1,0])) : 0}
    pos += [2,0]
    steps = {tuple(pos) : 2}
    i = 0;
    while i < 2000:
        # move_dir = (random()*4)//1 + 1
        # intcode.execute(move_dir, True);
        moveable = checkDir(grid, pos, intcode)
        if len(moveable) == 0:
            print('all has been explored');
            break;
        if len(moveable) == 1:
            grid[tuple(pos)] = -1;
            intcode.execute(moveable[0], True);
            move = moveable[0];
        else:
            foundmove = False;
            for di in moveable:
                hasunknown = False;
                for k in range(1,5):
                    if tuple(pos + move_dirs[di] + move_dirs[k]) not in grid:
                        hasunknown = True;
                        break;
                if hasunknown:
                    foundmove = True;
                    intcode.execute(di, True);
                    move = di;
                    break;
            if not foundmove:
                move_dir = int(random()*len(moveable));
                intcode.execute(moveable[move_dir], True);
                move = moveable[move_dir];
        pos += move_dirs[move];
        adjacentlocations = []
        for k in range(1,5):
            if tuple(pos + move_dirs[k]) in steps:
                adjacentlocations.append(steps[tuple(pos + move_dirs[k])]);
        steps[tuple(pos)] = min(adjacentlocations) + 1;
        if intcode.outputs[0] == 2:
            print('found');
            break;
        i += 1;
    print_grid(grid, pos);
    
    print("Day 15-2 answer is {0}".format(max(steps.values())));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
