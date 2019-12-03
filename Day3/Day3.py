# Day 1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% Read data
data = pd.read_csv('Input_Day3.txt', header=None).T;
#data = pd.read_csv('Test.txt', header=None).T;
data.columns = ['Wire1', 'Wire2']


class Coord:
    def __init__(self, x, y, step):
        self.x = x;
        self.y = y;
        self.step = step;
    def xy(self):
        return np.array([self.x,self.y]);

class Line:
    def __init__(self, start, dir_x, dir_y, len):
        self.start = start;
        self.dir_x = dir_x;
        self.dir_y = dir_y;
        self.len = len;
    def check_intersect(self, line):
        def between (check, cl1, cl2):
            if cl1 > cl2:
                cl3 = cl2;
                cl2 = cl1;
                cl1 = cl3;
            return (cl1 < check < cl2)
        
        if (self.dir_x != 0):
            if line.dir_x != 0:
                return False;
            if (between(line.start.x, self.start.x, self.start.x + self.dir_x * self.len)):
                if (between(self.start.y, line.start.y, line.start.y + line.dir_y * line.len)):
                    return True;
        else:
            if line.dir_y != 0:
                return False;
            if (between(line.start.y, self.start.y, self.start.y + self.dir_y * self.len)):
                if (between(self.start.x, line.start.x, line.start.x + line.dir_x * line.len)):
                    return True;
        
    def get_intersect(self,line):
        if (self.dir_x == 0):
            coord = Coord(self.start.x, line.start.y, 1)
            if (self.dir_y == 1):
                step1 = self.start.step + line.start.y - self.start.y;
            else:
                step1 = self.start.step + self.start.y - line.start.y;
            if (line.dir_x == 1):
                step2 = line.start.step + self.start.x - line.start.x;
            else:
                step2 = line.start.step + line.start.x - self.start.x;
        else:
            coord = Coord(line.start.x, self.start.y, 1);
            if (self.dir_x == 1):
                step1 = self.start.step + line.start.x - self.start.x;
            else:
                step1 = self.start.step + self.start.x - line.start.x;
            if (line.dir_x == 1):
                step2 = line.start.step + self.start.y - line.start.y;
            else:
                step2 = line.start.step + line.start.y - self.start.y;
        return coord, step1, step2
    def end(self):
        return Coord(self.start.x + self.dir_x * self.len, self.start.y + self.dir_y * self.len, self.start.step + self.len);
    def Draw(self, color):
        plt.plot([self.start.x, self.end().x], [self.start.y, self.end().y], color=color);


class Wire:
    def __init__(self, color):
        self.end = Coord(0,0,0);
        self.lines = np.empty([400,1], dtype='object')
        self.lineit = 0;
        self.color = color;
        
    def AddLine(self, command):
        dirr = self.getDir(command[0]);
        amount = int(command[1:]);
        this_line = Line(self.end, dirr[0], dirr[1], amount);
        this_line.Draw(self.color);
        self.lines[self.lineit] = this_line
        self.end = this_line.end();
        self.lineit += 1;
    def getDir(self, dirr):
        if (dirr == 'L'):
            return([-1,0]);
        elif (dirr == 'R'):
            return([1,0]);
        elif (dirr == 'U'):
            return([0,1]);
        elif (dirr == 'D'):
            return([0,-1]);
    def overlaps(self, wire):
        o_it = 0;
        overlaps = np.empty([50,1], dtype='object')
        step1 = np.empty([50,1], dtype='object')
        step2 = np.empty([50,1], dtype='object')
        for i in self.lines[self.lines != None]:
            for j in wire.lines[wire.lines != None]:
                if (i.check_intersect(j)):
                    overlaps[o_it], step1[o_it], step2[o_it] = i.get_intersect(j);                        
# =============================================================================
#                     plt.figure()
#                     i.Draw(self.color);
#                     j.Draw(wire.color);
#                     plt.scatter(overlaps[o_it][0].x, overlaps[o_it][0].y)
#                     plt.pause(1);
# =============================================================================
                    o_it += 1;
        step1 = step1[overlaps!=None];
        step2 = step2[overlaps!=None];
        overlaps = overlaps[overlaps!=None];
        return overlaps, step1, step2 
        

#%%

if (__name__ == '__main__'):
    import time
    t0 = time.time();
    wire1 = Wire([0,1,0]);
    wire2 = Wire([1,0,0]);
    
    for i in range(len(data.Wire1)):
        wire1.AddLine(data.Wire1[i]);
        
    for i in range(len(data.Wire2)):
        wire2.AddLine(data.Wire2[i]);
    
    dist = 100000;
    step = 100000;
    overlaps, step1, step2 = wire1.overlaps(wire2);
    for i in range(len(overlaps)):
        coord = overlaps[i];
        new_dist = abs(coord.x) + abs(coord.y);
        new_step = step1[i] + step2[i]
        dist = min(dist,new_dist);
        step = min(step,new_step);
        
            
    print("Day 3-1 answer is {0}".format(dist));
    
    
    
    print("Day 3-2 answer is {0}".format(step));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));