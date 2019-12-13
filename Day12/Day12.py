import time
t0 = time.time();

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import parse
#from Day9 import IntCode

class Moon:
    
    def __init__(self, x : int, y : int, z : int) -> type(None):
        self.pos = np.array([x,y,z]);
        self.init_pos = np.array([x,y,z]);
        self.vel = np.array([0,0,0]);
    
    def update_vel(self, moons : list) -> type(None):
        for moon in moons:
            if not self == moon:
                diff = moon.pos - self.pos;
                self.vel += np.sign(diff);
                
    def update_pos(self) -> type(None):
        self.pos += self.vel;
    
    def __repr__(self):
        return 'POS <X: {0} - Y: {1} - Z: {2}> - VEL <X: {3} - Y: {4} - Z: {5}>' \
        .format(self.pos[0], self.pos[1], self.pos[2], self.vel[0], self.vel[1], self.vel[2]);
    
    def energy(self) -> int:
        e_kin = abs(self.vel).sum();
        e_pot = abs(self.pos).sum();
        return e_kin * e_pot;
    
    # def isinit(self) -> bool:
    #     return np.all(self.pos == self.init_pos) and self.vel.sum() == 0;

def ReadMoons(data : pd.core.series.Series) -> list:
    coord_format = "x={0}, y={1}, z={2}>";
    moons = []
    for i in range(len(data)):
        coord = parse.parse(coord_format, data[i])
        x = int(coord[0]);
        y = int(coord[1]);
        z = int(coord[2]);
        moons.append(Moon(x, y, z));
    return moons;

#%%
if (__name__ == '__main__'):
    #Store in digits

    data = pd.read_csv('Input_Day12.txt', header=None, delimiter='<')[1];
    #data = pd.read_csv('Test.txt', header=None, delimiter='<')[1];
    #data = pd.read_csv('Test2.txt', header=None, delimiter='<')[1];
    moons = ReadMoons(data);
    
    t = 0;
    update_vel = lambda x : x.update_vel(moons);
    update_pos = lambda x : x.update_pos();
    while t < 1000:
        _ = list(map(update_vel, moons));
        _ = list(map(update_pos, moons));
        t+=1;

    
    energies = [moon.energy() for moon in moons]
    
    print("Day 12-1 answer is {0}".format(sum(energies)));
    t1= time.time();
    
    moons = ReadMoons(data);

    periods = np.zeros([4,6], dtype='int32');
    t = 0;
    t_max = 400000
    xs = np.zeros([4,t_max], dtype='int32')
    ys = np.zeros([4,t_max], dtype='int32')
    zs = np.zeros([4,t_max], dtype='int32')
    vxs = np.zeros([4,t_max], dtype='int32')
    vys = np.zeros([4,t_max], dtype='int32')
    vzs = np.zeros([4,t_max], dtype='int32')
    
    while t<t_max:
        for moon_i in range(len(moons)):
            xs[moon_i,t] = moons[moon_i].pos[0]
            ys[moon_i,t] = moons[moon_i].pos[1]
            zs[moon_i,t] = moons[moon_i].pos[2]
            vxs[moon_i,t] = moons[moon_i].vel[0]
            vys[moon_i,t] = moons[moon_i].vel[1]
            vzs[moon_i,t] = moons[moon_i].vel[2]
        _ = list(map(update_vel, moons));
        _ = list(map(update_pos, moons));
        t+=1;


    for moon_i in range(len(moons)):  
        series = dict(zip(range(6), [tuple(xs[moon_i,:]), tuple(ys[moon_i,:]), tuple(zs[moon_i,:]), \
                                     tuple(vxs[moon_i,:]), tuple(vys[moon_i,:]), tuple(vzs[moon_i,:])]));
        for serie_i in range(len(series)):
            serie = series[serie_i];
            for i in range(2, len(serie)//2):
                works = True;
                for j in range(i):
                    if serie[j] != serie[i+j]:
                        works = False;
                        break;

                        
                if works:
                    periods[moon_i, serie_i] = i;
                    break;
            
    
    plt.plot(range(len(zs[0,:])), zs[0,:])
    print(periods)
    periods = np.array(periods, dtype='int64')
    
    fit1 = np.lcm(periods[0,0], periods[0,1]);
    fit = np.lcm(fit1, periods[0,2]);
    
    print("Day 12-2 answer is {0}".format(fit));

    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
