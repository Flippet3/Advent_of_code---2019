import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import parse
import math
from Day9 import IntCode
    

def CheckPos(intcode, x, y):
    intcode.reset();
    intcode.execute(x, True);
    intcode.execute(y, True);
    return intcode.outputs[0];

def SetGrid(x,y,frac_low,frac_high):
    fig = plt.figure(1);
    ax = fig.add_subplot(1,1,1);
    grid = np.zeros([y,x]);
    for i_x in range(x):
        for i_y in range(y):
            if i_y == 0:
                if i_x != 0:
                    continue;
            elif not(frac_low < i_x/i_y < frac_high):
                continue;
            grid[i_y,i_x] = 1;
            # ax.scatter(i_x,i_y);
    ax.imshow(grid, cmap=cm.gray);
    return grid;

def SetGrid2(x_0, y_0, x_d,y_d):
    fig = plt.figure(2);
    ax = fig.add_subplot(1,1,1);
    grid = np.zeros([y_d,x_d]);
    for i_x in range(x_0, x_0+x_d):
        for i_y in range(y_0, y_0+y_d):
            if CheckPos(intcode,i_x,i_y) == 1:
                grid[i_y-y_0,i_x-x_0] = 1;
                ax.scatter(i_x,i_y);
    return grid;

def FindShip(x,y,frac_low,frac_high):
    def L1(x):
        return int((x)/frac_low);
    def L2(x):
        return int((x)/frac_high+1);
    fig = plt.figure(1);
    ax = fig.axes[0];
    x_1 = 10;
    found = False;
    while not found:
        x_2 = x_1+x-1;
        if L1(x_1)-L2(x_2)>=y-1:
            found = True;
        else:
            x_1 += 1;
    return [(x_1, L1(x_1)), (x_2, L2(x_2))];


#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day19.txt', header=None).T;
    data.columns=['opcode']
    intcode = IntCode(data.values.T[0]);
    
    margin = 0.1;
    frac_low = 0; #x/y
    while margin > 10e-7:
        y = 10e7;
        x = int(y * frac_low);
        o = CheckPos(intcode, x, y);
        if o == 0:
            frac_low += margin;
            continue
        else:
            margin *= 0.5;
            frac_low -= margin;
    
    margin = 0.1;
    frac_high = 1;
    while margin > 10e-7:
        y = 10e7;
        x = int(y * frac_high);
        o = CheckPos(intcode, x, y);
        if o == 0:
            frac_high -= margin;
            continue
        else:
            margin *= 0.5;
            frac_high += margin;
    grid = SetGrid(50,50,frac_low,frac_high);
    
    print("Day 19-1 answer is {0}".format(grid.sum()));
    t1 = time.time();
    
    coords = FindShip(100, 100, frac_low,frac_high);
    
    print("Day 19-2 answer is {0}".format(min(coords[0][0],coords[1][0])*10000+min(coords[0][1],coords[1][1])));

    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
