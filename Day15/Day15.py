import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
from Day9 import IntCode
from random import random;
    

            
def print_grid(grid):
    fig = plt.figure(1);
    ax = fig.add_subplot(1,1,1);
    for coord in grid:
        if grid[coord] == 0:
            color = 'r';
        elif grid[coord] == 1:
            color = 'g'
        ax.scatter(coord[0], coord[1], color=color);

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day15.txt', header=None).T;
    data.columns=['opcode']
    intcode = IntCode(data.values.T[0]);
    
    move_dirs = {1 : np.array([0,1]), 2 : np.array([0,-1]), 3 : np.array([-1,0]), 4 : np.array([1,0])}
    
    
    grid = {(0,0) : 1}
    pos = np.array([0,0])
    i = 0;
    while i < 10000:
        move_dir = (random()*4)//1 + 1
        intcode.execute(move_dir, True);
        target_pos = pos + move_dirs[move_dir];
        if tuple(target_pos) in grid:
            if grid[tuple(target_pos)] == 0:
                i += 1;
                continue;
        grid[tuple(target_pos)] = intcode.outputs[0];
        if intcode.outputs[0] == 1:
            pos = target_pos;
        elif intcode.outputs[0] == 2:
            break;
        i += 1;
    print_grid(grid);
    
            
    print("Day 15-1 answer is {0}".format(1));
    t1= time.time();

    
    print("Day 15-2 answer is {0}".format(1));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
