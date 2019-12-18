import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
#from Day9 import IntCode

class Agent:
    def __init__(self, pos, steps, keys):
        self.pos = pos;
        self.steps = steps;
        self.keys = keys;
    
    def __repr__(self):
        return 'Position: {0}\nSteps: {1}\nKeys: {2}'.format(self.pos, self.steps, self.keys);

class Grid:
    def __init__(self, values):
        self.grid = []
        self.Y = len(values);
        self.X = len(values[0])
        #UP, DOWN, LEFT, RIGHT;
        self.dirs = {1 : [0,1], 2 : [0,-1], 3 : [-1,0], 4 : [1,0]};
        for y in range(self.Y):
            gridline = []
            for x in range(self.X):
                if values[y][x] == '@':
                    self.pos = np.array([x,y]);
                    gridline.append('.');
                else:
                    gridline.append(values[y][x]);
            self.grid.append(gridline);
    
    def Get(self,*args):
        if len(args) == 1:
            args = args[0]
        return self.grid[args[1]][args[0]];
    
    def Set(self, *args):
        if len(args) == 2:
            pos = args[0];
            self.grid[pos[1], pos[0]] = args[1];
        else:
            self.grid[args[1]][args[0]] = args[2];
    
    def Reduce(self):
        final = False;
        while not final:
            final = True;
            for y in range(self.Y):
                for x in range(self.X):
                    if self.Get(x,y) == '.':
                        around = self.GetAround(np.array([x,y]));
                        if around.count('#') == 3:
                            self.Set(x,y,'#');
                            final = False;
                            print('reduced')
    
    def FindKeys(self, pos, keys):
        dirs = [1,2,3,4];
        visited = set();
        agents = {tuple(pos)}
        steps = 0;
        keys_found = set()
        while len(agents) >= 1:
            steps += 1;
            newagents = set()
            for agent in agents:
                visited.add(agent);
                around = self.GetAround(agent);
                for i in range(len(around)):
                    neighbor = around[i];
                    if neighbor == '#':
                        continue;
                    ag_pos = (agent[0] + self.dirs[i+1][0], agent[1] + self.dirs[i+1][1]);
                    if neighbor.isalpha():
                        if neighbor.isupper():
                            if not neighbor.lower() in keys:
                                continue;
                        else:
                            if not neighbor in keys:
                                keys_found.add((ag_pos, steps, neighbor));
                                continue;
                    if ag_pos not in visited:
                        newagents.add(ag_pos);
                #print ('inspected {0} from {1}'.format(agent, agents));
            agents = newagents
        return keys_found;
        
    def GetAround(self, pos):
        pos = np.array(pos);
        around = []
        for i in range(4):
            around.append(self.Get(pos + self.dirs[i+1]));
        return around;
    


#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day18.txt', header=None);
    #data = pd.read_csv('Test2.txt', header=None);
    data.columns = ['my_info']
    grid = Grid(data.my_info.values)
    grid.Reduce();
    
    converged = False
    # position, steps, keys;
    agents = [Agent(grid.pos, 0, set())];
    while not converged:
        doubleagents = [];
        newagents = [];
        for i in range(len(agents)):
            agent1 = agents[i];
            for j in range(i+1,len(agents)):
                agent2 = agents[j];
                if np.all(agent1.pos == agent2.pos) and agent1.keys == agent2.keys:
                    if agent1.steps > agent2.steps:
                        if agent1 not in doubleagents:
                            doubleagents.append(agent1);
                    else:
                        if agent2 not in doubleagents:
                            doubleagents.append(agent2);
        for i in range(len(doubleagents)):
            print("double agent removed");
            agents.remove(doubleagents[i]);
        for agent in agents:
            keys_grabable = grid.FindKeys(agent.pos, agent.keys);
            for key_info in keys_grabable:
                keys = agent.keys.copy();
                keys.add(key_info[2]);
                newagents.append(Agent(key_info[0], agent.steps + key_info[1], keys));
        if len(newagents) == 0:
            converged = True;
            break;
        else:
            agents = newagents;
        print(len(agents));
    
    
    print("Day 18-2 answer is {0}".format(agents[0].steps));
    t1 = time.time();



    print("Day 18-1 answer is {0}".format(1));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
