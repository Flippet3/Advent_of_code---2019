import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Day9 import IntCode

class Grid():
    def __init__(self):
        self.base = 0;
        self.grid = self.base * np.ones([1,1]);
        self.ball_pos = (0,0);
        self.racket_pos = (0,0);
    
    def add_point(self, x, y, tile_id):
        if x == -1:
            self.score = tile_id;
            return;
        if x >= self.grid.shape[1]:
            self.grid = np.append(self.grid, self.base * np.ones([self.grid.shape[0], x-self.grid.shape[1]+1]), axis=1);
        if y >= self.grid.shape[0]:
            self.grid = np.append(self.grid, self.base * np.ones([y-self.grid.shape[0]+1, self.grid.shape[1]]), axis=0);
        if (tile_id == 4):
            self.ball_pos = (y,x);
        if (tile_id == 3):
            self.racket_pos = (y,x);
        self.grid[y,x] = tile_id;
    
    def show(self):
        fig = plt.figure(1, figsize = (10,self.grid.shape[0]/self.grid.shape[1]*10))
        ax = fig.add_subplot(1,1,1);
        for x in range(self.grid.shape[1]):
            for y in range(self.grid.shape[0]):
                if self.grid[y,x] == 1:
                    color = 'g'
                elif self.grid[y,x] == 2:
                    color = 'r'
                elif self.grid[y,x] == 3:
                    color = 'b'
                elif self.grid[y,x] == 4:
                    color = 'k'
                if self.grid[y,x] != 0:
                    ax.scatter(self.grid.shape[1]-x,self.grid.shape[0]-y,color=color);
        ax.grid(True, which='major');
        ax.set_xticks(np.arange(0,ax.get_xlim()[1]));
        ax.set_yticks(np.arange(0,ax.get_ylim()[1]));
    

        
            

#%%
if (__name__ == '__main__'):
    #Store in digits
    plt.close('all')
    grid = Grid();
    data = pd.read_csv('Input_Day13.txt', header=None).T;
    data.columns=['opcode']
    data.opcode[0] = 2;
    intcode = IntCode(data.values.T[0]);
    intcode.execute(0, True);
    for i,item in enumerate(intcode.outputs):
        if (i%3==0):
            x = item;
        elif (i%3==1):
            y = item;
        elif (i%3==2):
            tile_id = item;
            grid.add_point(x,y,tile_id);
    grid.show();
            
    print("Day 13-1 answer is {0}".format((grid.grid==2).sum()));
    t1= time.time();
    
    it = 0;
    done = False;
    while not done:
        it += 1;
        if (grid.ball_pos[1] < grid.racket_pos[1]):
            action = -1;
        elif (grid.ball_pos[1] > grid.racket_pos[1]):
            action = 1;
        else:
            action = 0;
        intcode.execute(action, True);
        bla = 0;
        for i,item in enumerate(intcode.outputs):
            if (i%3==0):
                x = item;
            elif (i%3==1):
                y = item;
            elif (i%3==2):
                tile_id = item;
                if (tile_id >=3 or tile_id < -1):
                    bla += 1;
                grid.add_point(x,y,tile_id);
                if (x == -1 and (grid.grid==2).sum() == 0):
                    done = True;
                    
        if it%1000 == 0 or done:
            plt.cla()
            grid.show();    
            plt.pause(0.1);
    
    print("Day 13-2 answer is {0}".format(grid.score));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
