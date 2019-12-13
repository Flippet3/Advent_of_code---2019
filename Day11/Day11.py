import time
t0 = time.time();

# Day 1
import pandas as pd
import matplotlib.pyplot as plt
from Day9 import IntCode

def robot_walk(gridspaces, intcode):
    dirs = dict(zip(range(4), [(0,1), (1,0), (0,-1), (-1,0)]));
    my_dir = 0;
    robot_loc = [0,0];
    
    while True:
        if (tuple(robot_loc) in gridspaces):
            inp = gridspaces[tuple(robot_loc)];
        else:
            inp = 0;
        intcode.execute(inp,True)
        if len(intcode.outputs) == 0:
            break;
        p = intcode.outputs[0];
        my_dir = (my_dir + 2 * intcode.outputs[1] - 1)%4;
        gridspaces[tuple(robot_loc)] = p;
        robot_loc[0] += dirs[my_dir][0];
        robot_loc[1] += dirs[my_dir][1];
    return gridspaces;

#%%
if (__name__ == '__main__'):
    #Store in digits

    data = pd.read_csv('Input_Day11.txt', header=None).T;
    data.columns=['opcode']
    intcode = IntCode(data.values.T[0]);
    
    gridspaces = robot_walk({(0,0): 0}, intcode);
    
    print("Day 11-1 answer is {0}".format(len(gridspaces)));
    t1= time.time();
    
    intcode.reset();
    gridspaces = robot_walk({(0,0): 1}, intcode);
    
    plt.figure(figsize=(10,1))
    for i in gridspaces:
        if (gridspaces[i] == 1):
            c = 'r';
        else:
            c = 'g';
        plt.scatter(i[0], i[1], color=c, s = 100)
    
    print("Day 11-2 answer is {0}".format('see figure'));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
