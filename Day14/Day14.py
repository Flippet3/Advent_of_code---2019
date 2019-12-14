import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
#from Day9 import IntCode
    
# class for storing and showing recipe information.
class Recipe():
    def __init__(self, amount : int, name : str) -> type(None):
        self.name = name;
        self.produced = amount;
        self.requirements = []
        
    def add_requirement(self, requirement_amount : int, requirement : str):
        self.requirements.append((requirement_amount, requirement));
            
    def __repr__(self):
        my_str = '';
        for i in range(len(self.requirements)):
            if i != 0:
                my_str += ', ';
            my_str += str(self.requirements[i][0]) + ' ' + self.requirements[i][1];
        my_str += ' => ' + str(self.produced) + ' ' + self.name;
        return my_str
            
        

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day14.txt', header=None, delimiter='=>', engine='python');
    # data = pd.read_csv('Test.txt', header=None, delimiter='=>');
    data.columns=['inp', 'out'];
    format_string = '{:d} {}';
    
    # Store data in the form of recipes.
    recipes = {'ORE': Recipe(1,'ORE')}
    for i in range(len(data)):
        info = tuple(parse.parse(format_string, data.out[i]))
        my_recipe = Recipe(info[0], info[1]);
        inputs = data.inp[i].split(',');
        for j in range(len(inputs)):
            info2 = tuple(parse.parse(format_string, inputs[j]));
            if info2[1][-1] == ' ':
                my_recipe.add_requirement(info2[0], info2[1][:-1]);
            else:
                my_recipe.add_requirement(info2[0], info2[1]);
        recipes[info[1]] = my_recipe;
    
    # Make a request for 1 FUEL.
    requests = [(1,'FUEL')];
    items = {};
    oresused = 0;
    
    def processRequest(items, requests, oresused, recipes):
        while True:
            if len(requests) == 0:
                break;
            request = requests[-1];
            if request[1] not in items:
                items[request[1]] = 0;
            if request[1] == 'ORE':
                items['ORE'] += request[0];
                oresused += request[0]
                requests.remove(request);
                continue;
            hasItems = True;
            # Check if all items are present. If not, make a request for recipes.
            for requirement in recipes[request[1]].requirements:
                if not requirement[1] in items:
                    items[requirement[1]] = 0;
                if items[requirement[1]] < requirement[0] * (request[0]):
                    hasItems = False;
                    requests.append((math.ceil((requirement[0] * request[0] - items[requirement[1]])/recipes[requirement[1]].produced), requirement[1]));
                    break;
            # If all items are present, trasfer the items and remove the recipe request.
            if (hasItems):
                for requirement in recipes[request[1]].requirements:
                    items[requirement[1]] -= requirement[0] * request[0];
                items[request[1]] += request[0] * recipes[request[1]].produced;
                requests.remove(request);
        return oresused;
    
    oresused = processRequest(items, requests, oresused, recipes);
            
    print("Day 14-1 answer is {0}".format(oresused));
    t1= time.time();
    start_ores = 1000000000000;
    maxore_for_fuel = oresused;
    fuelcollected = 1;
    while True:
        # With no extra items, we know it took -maxore_for_fuel- to make 1 fuel
        # Thus it will take this at max. We can safely request the amount of fuel
        # made with that many ores.
        ores_left = start_ores - oresused;
        fuel_target = max(ores_left//maxore_for_fuel,1);
        requests = [(fuel_target,'FUEL')];
        oresused = processRequest(items, requests, oresused, recipes);
        if oresused > start_ores:
            break;
        else:
            fuelcollected += fuel_target;
    
    
    
    print("Day 14-2 answer is {0}".format(fuelcollected));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
