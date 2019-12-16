import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
#from Day9 import IntCode
    

            
    
    

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day16.txt', header=None);
    #data = pd.read_csv('Test.txt', header=None);
    digit_str = data[0][0];
    digit_len = len(digit_str);
    digit = np.array([int(i) for i in digit_str]).T;
    
    # Create multiplication code.
    multicode = np.zeros([digit_len, digit_len]);
    multicode_base = [0,1,0,-1];
    for i in range(digit_len):
        layer_multicode = [item for item in multicode_base for j in range(i+1)];
        layer_multicode *= digit_len//len(layer_multicode) + 1;
        multicode[i,:] = layer_multicode[1:digit_len + 1];
        # layer_i = mult
    
    iteration = 0;
    while iteration < 100:
        result_m = multicode * digit;
        digit = abs(result_m.sum(axis=1))%10
        
        iteration += 1;
    
    
            
    print("Day 16-1 answer is {0}".format(digit[0:8]));
    t1= time.time();
    
    
    print("Day 16-2 answer is {0}".format(1));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
