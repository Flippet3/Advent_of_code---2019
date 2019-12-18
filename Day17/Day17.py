import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
from Day9 import IntCode
from random import random;
    

def CheckScaffold(grid, pos):
    if not (0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])):
        return False;
    if not grid[pos[0]][pos[1]] == '#':
        return False;
    return True;

def printasciilist (my_list):
    my_str = '';
    for i in range(len(my_list)):
        my_str += chr(my_list[i]);
    print(my_str);

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day17.txt', header=None).T;
    data.columns=['opcode']
    intcode = IntCode(data.values.T[0]);
    intcode.execute(0);
    output = intcode.outputs;
    grid = [];
    gridline = '';
    for i in range(len(output)):
        if output[i] == 10:
            if i != len(output)-1:
                grid.append(gridline);
                gridline = '';
            continue;
        gridline += chr(output[i]);
    allignmentparams = []
    for y in range(0,len(grid)):
        for x in range(0,len(grid[0])):
            if 1 < y < len(grid) - 1 and 1 < x < len(grid) - 1:
                if grid[y][x] == '#':
                    if grid[y-1][x] == '#' and\
                        grid[y+1][x] == '#' and\
                            grid[y][x+1] == '#' and\
                                grid[y][x-1] == '#':
                                    allignmentparams.append(y*x);
            if grid[y][x] in '^><v':
                move_dir = dict(zip('><v^', range(1,5)))[grid[y][x]];
                pos = np.array([y,x]);
            
    print("Day 17-1 answer is {0}".format(sum(allignmentparams)));
    
            # East, West, South, North
    move_dirs  = {1 : np.array([0,1]), 2 : np.array([0,-1]), 3 : np.array([1,0]), 4 : np.array([-1,0])}
    right_dirs = {1 : 3, 2 : 4, 3 : 2, 4 : 1};
    left_dirs  = {1 : 4, 2 : 3, 3 : 1, 4 : 2};
    t1= time.time();
    
    
    
    # Create path
    path = ''
    
    reached_end = False;
    while not reached_end:
        travelabledist = 0;
        end = False;
        while not end:
            if not (CheckScaffold(grid, pos + move_dirs[move_dir])):
                end = True;
                continue;
            else:
                pos += move_dirs[move_dir];
                travelabledist += 1;
        if travelabledist != 0:
            path += (str(travelabledist));
        if CheckScaffold(grid, pos + move_dirs[right_dirs[move_dir]]):
            path += ('R');
            move_dir = right_dirs[move_dir];
        elif CheckScaffold(grid, pos + move_dirs[left_dirs[move_dir]]):
            path += ('L');
            move_dir = left_dirs[move_dir];
        else:
            reached_end=True;
            continue;
    
    #path = 'R8R8R4R4R8L6L2R4R4R8R8R8L6L2'
    maxnr = 12;
    
    for i in range(2,maxnr):
        A = path[0:i];
        if (path[i] == '0'):
            continue;
        Apath = 'A'
        ii = i;
        j_low = 100;
        while ii <= len(path) - i:
            if path[ii:ii+i] == A:
                Apath += 'A';
                ii += i;
            else:
                j_low = min(len(Apath),j_low);
                Apath += path[ii];
                ii += 1;
        Apath += path[ii:];
        if j_low == 100:
                j_low = 1;
        # print('A: {0}'.format(A));
        # print(Apath);
        for j in range(2,maxnr):
            B = Apath[j_low:j+j_low];
            if ('A' in B) or (Apath[j_low+j] == '0'):
                continue;
            Bpath = Apath[0:j_low] + 'B'
            jj = j_low + j;
            k_low = 100;
            while jj <= len(Apath) - j:
                if Apath[jj:jj+j] == B:
                    Bpath += 'B';
                    jj += j;
                else:
                    if (Apath[jj] not in 'A'):
                        k_low = min(len(Bpath),k_low);
                    Bpath += Apath[jj];
                    jj += 1;
            if k_low == 100:
                k_low = 1;
            Bpath += Apath[jj:];
            # print('B: {0}'.format(B));
            # print(Bpath);
            for k in range(2,maxnr):
                C = Bpath[k_low:k_low+k];
                if ('A' in C) or ('B' in C) or (Bpath[k_low+k] == '0'):
                    continue;
                Cpath = Bpath[0:k_low] + 'C'
                kk = k_low + k;
                succes = True;
                while kk <= len(Bpath) - k:
                    if Bpath[kk:kk+k] == C:
                        Cpath += 'C';
                        kk += k;
                    else:
                        Cpath += Bpath[kk];
                        if Bpath[kk] not in 'AB':
                            succes = False;
                            #break;
                        kk += 1;
                Cpath += Bpath[kk:];
                # print('C: {0}'.format(C));
                # print(Cpath);
                # if not 'L' in Cpath and not 'R' in Cpath:
                #     print(Cpath);
                #     print('wow');
                if succes:
                    print('======SUCCES=======\nA : {0}\nB : {1}\nC : {2}\n{3}'.format(A,B,C,Cpath));
                    A_found = A;
                    B_found = B;
                    C_found = C;
                    path_found = Cpath;
                    break;
        
        
    intcode.reset();
    intcode.cur_memory[0] = 2;
    
    #intcode.execute(0)
    for i in range(4):
        my_str = [path_found,A_found,B_found,C_found][i];
        for j in range(len(my_str)):
            intcode.execute(ord(my_str[j]), True)
            if j != len(my_str)-1 and my_str[j] != '1':
                intcode.execute(ord(','), True);
        intcode.execute(10, True);
        print('========');
        printasciilist(intcode.outputs);
    intcode.execute(ord('n'), True);
    intcode.execute(10, True);
    printasciilist(intcode.outputs);
    
    print("Day 17-2 answer is {0}".format(intcode.outputs[-1]));

    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
