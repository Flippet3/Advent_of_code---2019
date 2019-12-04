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
    
    def CheckDouble(self, next_dig):
        if self.value == next_dig:
            return True;
        if self.pos != 'front':
            return self.prev_digit.CheckDouble(self.value);
        return False;
    
    def CheckDoubleNotTripple(self, next_dig):
        if self.value == next_dig:
            if (self.pos == 'front' or self.prev_digit.value != self.value):
                return True;
            dig = self;
            while dig.prev_digit.value == dig.value:
                if (dig.prev_digit.pos == 'front'):
                    return False;
                else:
                    dig = dig.prev_digit;
            return dig.prev_digit.CheckDoubleNotTripple(dig.value);
            
            
        if self.pos != 'front':
            return self.prev_digit.CheckDoubleNotTripple(self.value);
        return False;
    
    def CheckAscending(self, next_dig):
        if self.value <= next_dig:
            if self.pos == 'front':
                return True;
            return self.prev_digit.CheckAscending(self.value);
        return False;

    def IndexAllowed(self, nottripple = False):
        if (self.atlimit()):
            return False;
        if (self.pos=='back'):
            if not (nottripple):
                if (self.prev_digit.CheckDouble(self.value) and self.prev_digit.CheckAscending(self.value)):
                    return True;
            else:
                if (self.prev_digit.CheckDoubleNotTripple(self.value) and self.prev_digit.CheckAscending(self.value)):
                    return True;
        return False;
            
    def up(self):
        self.value = (self.value + 1) % 10;
        if self.value == 0:
            self.prev_digit.up();



# ugly function for printing
def printdigit(ldig):
    print(str(last_digit.prev_digit.prev_digit.prev_digit.prev_digit.prev_digit.value)+
          str(last_digit.prev_digit.prev_digit.prev_digit.prev_digit.value)+
          str(last_digit.prev_digit.prev_digit.prev_digit.value)+
          str(last_digit.prev_digit.prev_digit.value)+
          str(last_digit.prev_digit.value)+
          str(last_digit.value))


#%%
if (__name__ == '__main__'):
    #Store in digits
    data = pd.read_csv('Input_Day4.txt', header=None).T;
    n1,n2 = data[0][0].split('-')
    #n1 = '110800';
    #n2 = '112100';
    for i in range(len(n1)):
        if i == 0:
            prev_digit = Digit(int(n1[i]), 'front', int(n2[i]))
        elif i == len(n1)-1:
            last_digit = Digit(int(n1[i]), 'back', int(n2[i]), prev_digit)
        else:
            prev_digit = Digit(int(n1[i]), 'middle', int(n2[i]), prev_digit)
    

        
    possible_digits_1 = 0;
    possible_digits_2 = 0;
    while not last_digit.atlimit():
        last_digit.up();
        if (last_digit.IndexAllowed()):
            possible_digits_1 += 1;
        if (last_digit.IndexAllowed(True)):
            possible_digits_2 += 1;
            #printdigit(last_digit);
    
    print("Day 3-1 answer is {0}".format(possible_digits_1));
    
    
    
    print("Day 3-2 answer is {0}".format(possible_digits_2));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));