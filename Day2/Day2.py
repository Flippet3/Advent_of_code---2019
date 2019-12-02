import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd

#%%

class OpCode:
    # Params
    #base_memory;
    #cur_memory;
    
    def __init__(self, memory):
        self.base_memory = memory;
        self.reset();
    
    def execute(self, noun, verb):
        self.cur_memory[1] = noun;
        self.cur_memory[2] = verb;
        while True:
            if (self.cur_memory[self.instruction_pointer] == 1):
                self.cur_memory[self.cur_memory[self.instruction_pointer+3]] = self.cur_memory[self.cur_memory[self.instruction_pointer+1]] + self.cur_memory[self.cur_memory[self.instruction_pointer+2]];
                d_instruction_pointer = 4;
            elif (self.cur_memory[self.instruction_pointer] == 2):
                self.cur_memory[self.cur_memory[self.instruction_pointer+3]] = self.cur_memory[self.cur_memory[self.instruction_pointer+1]] * self.cur_memory[self.cur_memory[self.instruction_pointer+2]];
                d_instruction_pointer = 4;
            elif(self.cur_memory[self.instruction_pointer] == 99):
                break;
            self.instruction_pointer += d_instruction_pointer;
        return self.cur_memory[0];
        
    def reset(self):
        self.instruction_pointer = 0;
        self.cur_memory = self.base_memory.copy()

#%% Read data
data = pd.read_csv('Input_Day2.txt', header=None).T;
data.columns=['opcode']
#data.opcode[1] = 12; data.opcode[2] = 2;

# Test
#data = pd.DataFrame([1,0,0,0,99], columns=['opcode'])
#data = pd.DataFrame([2,3,0,3,99], columns=['opcode'])

#%% Initiate Opcode
opCode = OpCode(data.opcode)

#%% Part 1 Run the opcode
result1 = opCode.execute(12,2);

print("Day 2-1 answer is {0}".format(result1));

#%% Part 2
found = False
for i in range(101):
    for j in range(101):
        opCode.reset();
        zero_value = opCode.execute(i,j);
        if (zero_value == 19690720):
            found = True;
            break;
    if (found):
        break;
result2 = 100 * i + j;
print("Day 2-2 answer is {0}".format(result2));




#%%
t1 = time.time();
print ("Programme took {0} seconds to run".format(t1-t0));