import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
from Day9 import IntCode
from random import random;
    


    

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day17.txt', header=None).T;
    data.columns=['opcode']
    intcode = IntCode(data.values.T[0]);
    intcode.execute(0);
    output = intcode.outputs;

    print("Day 17-1 answer is {0}".format(1));
    
            
    move_dirs = {1 : np.array([0,1]), 2 : np.array([0,-1]), 3 : np.array([-1,0]), 4 : np.array([1,0])}
    t1= time.time();

    
    print("Day 17-2 answer is {0}".format(1));

    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
