import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



class Digit:
    def __init__ (self, value, pos, higher_bound, prev_digit=None):
        self.value = value;
        assert(pos in 'backfrontmiddle')
        self.pos = pos;
        self.hb = higher_bound;
        if pos != 'front':
            self.prev_digit = prev_digit;
    
    def atlimit(self):
        if self.value != self.hb:
            return False;
        else:
            if (self.pos == 'front' or (self.pos != 'front' and self.prev_digit.atlimit())):
                return True;
        return False;
    
    def CheckDouble(self, digits):
        if self.value in digits:
            return True;
        if self.pos != 'front':
            digits = digits + [self.value];
            return self.prev_digit.CheckDouble(digits);
        return False;
        
    def nextIndexAllowed(self):
        if (self.atlimit()):
            return False;
        if (self.pos=='back'):
            if (self.prev_digit.CheckDouble([self.value])):
                return True;
        return False;
            
    def up(self):
        self.value = (self.value + 1) % 10;
        if self.value == 0:
            self.prev_digit.up();






#%%
if (__name__ == '__main__'):
    data = pd.read_csv('Input_Day4.txt', header=None).T;
    n1,n2 = data[0][0].split('-')
    #n1 = '123456';
    #n2 = '123800';
    for i in range(len(n1)):
        if i == 0:
            prev_digit = Digit(int(n1[i]), 'front', int(n2[i]))
        elif i == len(n1)-1:
            last_digit = Digit(int(n1[i]), 'back', int(n2[i]), prev_digit)
        else:
            prev_digit = Digit(int(n1[i]), 'middle', int(n2[i]), prev_digit)
    
    def printdigit(ldig):
        print(str(last_digit.prev_digit.prev_digit.prev_digit.prev_digit.prev_digit.value)+
              str(last_digit.prev_digit.prev_digit.prev_digit.prev_digit.value)+
              str(last_digit.prev_digit.prev_digit.prev_digit.value)+
              str(last_digit.prev_digit.prev_digit.value)+
              str(last_digit.prev_digit.value)+
              str(last_digit.value))
    def nextdigit():
        last_digit.up();
        if (last_digit.nextIndexAllowed()):
            return;
        else:
            if (last_digit.atlimit()):
                return;
            nextdigit();
        
    possible_digits = 1;
    while not last_digit.atlimit():
        nextdigit();
        #printdigit(last_digit);
        possible_digits += 1;
    
    print("Day 3-1 answer is {0}".format(possible_digits));
    
    
    
    print("Day 3-2 answer is {0}".format(1));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));