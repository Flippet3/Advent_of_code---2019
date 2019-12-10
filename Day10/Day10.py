import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations
from math import atan2

class Field:
    def __init__(self, field_array: np.ndarray) -> type(None):
        self.field = field_array;
        self.width = len(self.field[0]);
        self.height = len(self.field);
    
    def Get(self, x, y):
        return self.field[y][x];

#%%
if (__name__ == '__main__'):
    #Store in digits
    data = pd.read_csv('Input_Day10.txt', header=None);
    data.columns=['field']
    field = Field(data.field.values);
#    field = Field(np.array(['......#.#.',
#    '#..#.#....',
#    '..#######.',
#    '.#.#.###..',
#    '.#..#.....',
#    '..#....#.#',
#    '#..#....#.',
#    '.##.#..###',
#    '##...#..#.',
#    '.#....####']))
#    field = Field(np.array(['#####', '##x##', '#####']));
    #field = Field(np.array(['###']));
    
    def isInt(var : float) -> bool:
        return var.is_integer()
    
    can_see = np.zeros((field.height, field.width));
    for i in range(field.width*field.height-1):
        x_i = i%field.width;
        y_i = int(i/field.width);
        if (field.Get(x_i, y_i) == '#'):
            for j in range(i+1, field.width*field.height):
                x_j = j%field.width;
                y_j = int(j/field.width);
                if (field.Get(x_j, y_j) == '#'):
                    dx = x_j - x_i;
                    dy = y_j - y_i;
                    clear = True;
                    if (dx!=0 and (dy==0 or abs(dx) < abs(dy))):
                        for k in range(abs(dx)-1, 0, -1): 
                            if isInt(dy*k/abs(dx)):
                                if (field.Get(x_i+int(k*dx/abs(dx)), y_i+int(dy*k/abs(dx))) == '#'):
                                    clear=False;
                    else:
                        for k in range(abs(dy)-1, 0, -1):
                            if isInt(dx*k/dy):
                                if (field.Get( x_i+int(dx*k/abs(dy)), y_i+int(k*dy/abs(dy))) == '#'):
                                    clear=False;
                    if (clear):
                        can_see[y_i, x_i] += 1;
                        can_see[y_j, x_j] += 1;
                                
                            

        
    print("Day 10-1 answer is {0}".format(can_see.max()));
    
    max_i = can_see.argmax();
    x_i = max_i%field.width;
    y_i = int(max_i/field.width);
    
    #destroyed_after_circle = 0;
    target = 200;
    can_see2 = np.zeros((field.height, field.width));
    for j in range(field.width*field.height):
        if (j==max_i):
            continue;
        x_j = j%field.width;
        y_j = int(j/field.width);
        if (field.Get(x_j, y_j) == '#'):
            dx = x_j - x_i;
            dy = y_j - y_i;
            clear = True;
            if (dx!=0 and (dy==0 or abs(dx) < abs(dy))):
                for k in range(abs(dx)-1, 0, -1): 
                    if isInt(dy*k/abs(dx)):
                        if (field.Get(x_i+int(k*dx/abs(dx)), y_i+int(dy*k/abs(dx))) == '#'):
                            clear=False;
            else:
                for k in range(abs(dy)-1, 0, -1):
                    if isInt(dx*k/dy):
                        if (field.Get( x_i+int(dx*k/abs(dy)), y_i+int(k*dy/abs(dy))) == '#'):
                            clear=False;
            if (clear):
                can_see2[y_j, x_j] += (atan2(dy,dx)+np.pi/2) % (2*np.pi)+0.0001;
    
    values = np.array([i for i in np.nditer(can_see2) if i != 0]);
    values.sort();
    two_hundo = np.where(can_see2 == values[199], 1, 0);
    coord = two_hundo.argmax();
    x_j = coord%field.width;
    y_j = int(coord/field.width);
    print("Day 10-2 answer is {0}".format(100*x_j+y_j));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
