import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd



#%% Functions
def fuel_required (mass):
    return max(int(mass/3)-2,0);


#%% Read data
data = pd.read_csv('Input_Day1.txt', names = ['mass'], header=None);


#%% Part 1
data['fuel'] = data.mass.apply(fuel_required);

total_fuel = data.fuel.sum();
print("Day 1-1 answer is {0}".format(total_fuel));


#%% Part 2
data['total_fuel'] = data.fuel
it = 0;
while it < 10000:
    it += 1;
    data.fuel = data.fuel.apply(fuel_required);
    data.total_fuel = data.total_fuel + data.fuel;
    if data.fuel.nunique() == 1 and data.fuel[0] == 0:
        break;

if not (it < 10000):
    print("don't trust these results")
total_fuel2 = data.total_fuel.sum();
print("Day 1-2 answer is {0}".format(total_fuel2));





t1 = time.time();
print ("Programme took {0} seconds to run".format(t1-t0));