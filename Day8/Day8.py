import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import permutations


def SPI2Array (SPI : str, width : int, height: int) -> np.ndarray:
    arr = np.array([int(SPI[i]) for i in range(len(SPI))])
    arr = np.reshape(arr, (-1, height, width));
    return arr;
    


#%%
if (__name__ == '__main__'):
    #Store in digits
    data = pd.read_csv('Input_Day8.txt', header=None);
    SPI = str(data[0].values[0]);
    width = 25; height = 6;
    im = SPI2Array(SPI, width, height)
    depth = im.shape[0];
    imnot0 = np.where(im!=0, 1, 0);
    imnot0 = np.sum(imnot0, axis=1);
    imnot0 = np.sum(imnot0, axis=1);
    best_layer = im[np.argmax(imnot0),:,:];
    
    result1 = sum([1 for i in np.nditer(best_layer) if i == 1]) * sum([1 for i in np.nditer(best_layer) if i == 2]);
        
    print("Day 8-1 answer is {0}".format(result1));
    
    final_im = np.zeros_like(best_layer);
    for x in range(width):
        for y in range(height):
            i = 0;
            while im[i,y,x] == 2:
                i+=1;
                assert(i!=depth);
            final_im[y,x] = im[i,y,x];
            
    plt.imshow(final_im, cmap=cm.gray, vmin=0, vmax=1)
    
    print("Day 8-2 answer is {0}".format('JCRCB'));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));