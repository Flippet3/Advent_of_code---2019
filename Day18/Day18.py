import time
t0 = time.time();

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parse
import math
#from Day9 import IntCode
    

            
def diglist2num (i_diglist) -> int:
    return sum(i_diglist * 10**np.arange(len(i_diglist)-1, -1, -1));
    

#%%
if (__name__ == '__main__'):
    #Load data.
    plt.close('all')
    data = pd.read_csv('Input_Day16.txt', header=None);
    #data = pd.read_csv('Test2.txt', header=None);
    digit_str = data[0][0];
    digit_len = len(digit_str);
    digit = np.array([int(i) for i in digit_str], dtype='int32').T;
    
    # Create multiplication code.
    multicode = np.zeros([digit_len, digit_len], dtype='int32');
    multicode_base = np.array([0,1,0,-1], dtype='int32');
    for i in range(digit_len):
        layer_multicode = np.repeat(multicode_base, i+1);
        tile_nr = digit_len//len(layer_multicode) + 1;
        if (tile_nr > 1):
            layer_multicode = np.tile(layer_multicode, tile_nr);
        multicode[i,:] = layer_multicode[1:digit_len + 1];
    
    
    phase = 100;
    iteration = 0;
    while iteration < phase:
        result_m = multicode * digit;
        digit = abs(result_m.sum(axis=1))%10
        iteration += 1;
    
            
    print("Day 16-1 answer is {0}".format(diglist2num(digit[0:8])));
    t1= time.time();
    digit_str = data[0][0] * 10000;
    digit = np.array([int(i) for i in digit_str], dtype='int32').T;
    offset = diglist2num(digit[0:7]);
    assert(offset > 0.5 * digit_len);
    digit = digit[offset:];
    
    iteration = 0
    while iteration < phase:
        digit = np.flip(np.cumsum(np.flip(digit)))%10;
        iteration += 1;
    
    print("Day 16-2 answer is {0}".format(diglist2num(digit[0:8])));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));
