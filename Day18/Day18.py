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
        self.keys_in_field = set();
        self.pos = [];
        for y in range(self.Y):
            gridline = []
            for x in range(self.X):
                if values[y][x] == '@':
                    self.pos.append((x,y));
                    newap = '@' + str(len(self.pos));
                    gridline.append(newap);
                    self.keys_in_field.add(newap);
                else:
                    if values[y][x].isalpha() and values[y][x].islower():
                        self.keys_in_field.add(values[y][x]);
                    gridline.append(values[y][x]);
            self.grid.append(gridline);
        self.keys_in_field = np.array(list(self.keys_in_field));
        self.grid = np.array(self.grid);
        self.FillMatrices();
    
    def print(self):
        for y in range(self.Y):
            gridline = ''
            for x in range(self.X):
                gridline += grid.grid[y][x];
            print(gridline + '\n')
    
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
        reduced = 0;
        while not final:
            final = True;
            for y in range(self.Y):
                for x in range(self.X):
                    if self.Get(x,y) == '.':
                        around = self.GetAround([x,y]);
                        if around.count('#') == 3:
                            self.Set(x,y,'#');
                            final = False;
                            reduced += 1;
        print('Reduced the grid by {0} steps'.format(reduced));
    
    def FindKeys(self, keys, *args):
        if len(args[0]) == 1:
            key = args[0];
        else:
            key = self.Get(args[0]);
        dirs = [1,2,3,4];
        visited = set();
        results = [];
        key_ind = np.where(self.keys_in_field == key)[0][0];
        for i,other_key in enumerate(self.keys_in_field):
            if (i!=key_ind) and not other_key in keys:
                cur_set = self.key_req_mat[key_ind][i];
                if len(cur_set.intersection(keys)) == len(cur_set):
                    results.append([other_key, self.steps_req_mat[key_ind][i]]);
        return results;
    
    def GetKeyInfo(self, key):
        keys_req_list = np.array([set() for i in range(len(self.keys_in_field))]);
        steps_req_list = np.zeros(len(self.keys_in_field));
        pos = self.GetPos(key);
        dirs = [1,2,3,4];
        visited = set();
        agents = [[tuple(pos),{key}]]
        steps = 0;
        keys_found = set()
        while len(agents) >= 1:
            steps += 1;
            newagents = [];
            for agent in agents:
                visited.add(agent[0]);
                around = self.GetAround(agent[0]);
                for i in range(len(around)):
                    neighbor = around[i];
                    if neighbor == '#':
                        continue;
                    ag_pos = (agent[0][0] + self.dirs[i+1][0], agent[0][1] + self.dirs[i+1][1]);
                    if ag_pos in visited:
                        continue;
                    if neighbor.isalpha() or neighbor[0] == '@':
                        if not neighbor[0].isupper() or neighbor[0] == '@':
                            keys_req_list[self.keys_in_field==neighbor]=agent[1];
                            steps_req_list[self.keys_in_field==neighbor]=steps;
                        agent[1] = agent[1].copy();
                        agent[1].add(neighbor.lower());
                    newagents.append([ag_pos,agent[1]]);
            agents = newagents
        return keys_req_list, steps_req_list;
    
    def GetAround(self, pos):
        pos = np.array(pos);
        around = []
        for i in range(4):
            around.append(self.Get(pos + self.dirs[i+1]));
        return around;
    
    def GetPos(self, key):
        ind = np.where(self.grid == key);
        pos = (ind[1][0], ind[0][0]);
        return pos;
    
    def FillMatrices(self):
        self.key_req_mat = np.array([set() for i in range(len(self.keys_in_field) * len(self.keys_in_field))]).reshape(len(self.keys_in_field),len(self.keys_in_field));
        self.steps_req_mat = np.zeros([len(self.keys_in_field),len(self.keys_in_field)]);
        for i,key in enumerate(self.keys_in_field):
            [keys_req_list, steps_req_list] = self.GetKeyInfo(key);
            for req_i,key_req in enumerate(keys_req_list):
                if len(key_req) == 0:
                    keys_req_list[req_i] = {'block'};
            self.key_req_mat[i,:] = keys_req_list;
            self.steps_req_mat[i,:] = steps_req_list;
            
def ReduceAgents(agents):
    doubleagents = [];
    for i in range(len(agents)):
        agent1 = agents[i];
        for j in range(i+1,len(agents)):
            agent2 = agents[j];
            if agent1.keys == agent2.keys and (agent1.pos == agent2.pos):
                if agent1.steps > agent2.steps:
                    if agent1 not in doubleagents:
                        doubleagents.append(agent1);
                else:
                    if agent2 not in doubleagents:
                        doubleagents.append(agent2);
    for i in range(len(doubleagents)):
        agents.remove(doubleagents[i]);
    print("{0} double agents removed".format(len(doubleagents)));
    return agents;

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    
    data = pd.read_csv('Input_Day18.txt', header=None);
    #data = pd.read_csv('Test3.txt', header=None);
    data.columns = ['my_info']
    grid = Grid(data.my_info.values)
    grid.Reduce();
    grid.print();

    
    converged = False
    # position, steps, keys;
    agents = [Agent(grid.pos, 0, {'@1', '@2', '@3', '@4'})];
    while not converged:
        agents = ReduceAgents(agents);
        newagents = [];
        for agent in agents:
            for i,pos in enumerate(agent.pos):
                keys_grabable = grid.FindKeys(agent.keys, pos);
                for key_info in keys_grabable:
                    keys = agent.keys.copy();
                    keys.add(key_info[0]);
                    poss = agent.pos.copy();
                    poss[i] = grid.GetPos(key_info[0]);
                    newagents.append(Agent(poss, agent.steps + key_info[1], keys));
        if len(newagents) == 0:
            converged = True;
            agents = ReduceAgents(agents);
            break;
        else:
            agents = newagents;
        print(len(agents));
    
    loweststeps = 10e10;
    for agent in agents:
        loweststeps = min(loweststeps, agent.steps);
    
    print("Day 18-1 answer is {0}".format(loweststeps));
    t1 = time.time();
    
    #%%
    data = pd.read_csv('Input_Day18_2.txt', header=None);
    #data = pd.read_csv('Test3.txt', header=None);
    data.columns = ['my_info']
    grid = Grid(data.my_info.values)
    grid.Reduce();
    grid.print();

    
    converged = False
    # position, steps, keys;
    agents = [Agent(grid.pos, 0, {'@1', '@2', '@3', '@4'})];
    while not converged:
        agents = ReduceAgents(agents);
        newagents = [];
        for agent in agents:
            for i,pos in enumerate(agent.pos):
                keys_grabable = grid.FindKeys(agent.keys, pos);
                for key_info in keys_grabable:
                    keys = agent.keys.copy();
                    keys.add(key_info[0]);
                    poss = agent.pos.copy();
                    poss[i] = grid.GetPos(key_info[0]);
                    newagents.append(Agent(poss, agent.steps + key_info[1], keys));
        if len(newagents) == 0:
            converged = True;
            agents = ReduceAgents(agents);
            break;
        else:
            agents = newagents;
        print(len(agents));
    
    loweststeps = 10e10;
    for agent in agents:
        loweststeps = min(loweststeps, agent.steps);
    
    print("Day 18-2 answer is {0}".format(loweststeps));
    t1 = time.time();

    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
