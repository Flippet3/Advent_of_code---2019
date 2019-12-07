import time
t0 = time.time();

# Day 1
import pandas as pd
import matplotlib.pyplot as plt

class Planet ():
    
    def __init__(self, name : str) -> type(None):
        self.name = name;
        self.hasorbiting = [];
        self.orbits = []
        self.distance = 10000;
    
    def __add__(self, other) -> type(None):
        self.hasorbiting.append(other);
        other.orbits.append(self);
    def __repr__(self) -> str:
        return "name = " + self.name;
    def broadcast_distance(self, dist_message : int) -> type(None):
        if (dist_message < self.distance):
            self.distance = dist_message + 1;
            [planet.broadcast_distance(self.distance) for planet in self.hasorbiting];
            [planet.broadcast_distance(self.distance) for planet in self.orbits];
    def __setitem__(self, key, value):
        self[key] = value;
        



#%%
if (__name__ == '__main__'):
    #Store in digits
    data = pd.read_csv('Input_Day6.txt', header=None, names=['center', 'orbiter'], sep=")");
    #data = pd.read_csv('Test.txt', header=None, names=['center', 'orbiter'], sep=")");
    
    planets = {}
    for i in range(len(data.center)):
        cen = data.center[i];
        orb = data.orbiter[i];
        if cen in planets:
            cen = planets[cen];
        else:
            cen = Planet(cen);
            planets[cen.name] = cen;
        if orb in planets:
            orb = planets[orb];
        else:
            orb = Planet(orb);
            planets[orb.name] = orb;
        cen + orb;
    
    planets['COM'].broadcast_distance(-1);
    
    dist = [planet.distance for planet in planets.values()];
    
    print("Day 6-1 answer is {0}".format(sum(dist)));
    
    for planet in planets.values():
        planet.distance = 10000;
    
    planets['YOU'].broadcast_distance(-1);
    
    print("Day 6-2 answer is {0}".format(planets['SAN'].distance - 2));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));