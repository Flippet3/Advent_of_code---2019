import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations


class IntCode:
    def __init__(self, memory: np.ndarray) -> type(None):
        self.base_memory = memory;
        self.reset();
        self.d_instruction_pointers = dict(zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 99], [4, 4, 2, 2, 3, 3, 4, 4, 2, 2]));
    
    def execute(self, i_input : int, i_phase : int = None, breakatoutput : bool = False) -> int:
        self.input = i_input;
        self.phase = i_phase;
        self.outputs = [];
        self.indices = [0 for i in range(3)];
        while True:
            opcode = self.cur_memory[self.instruction_pointer]%100;
            if (opcode == 99):
                break;
            d_instruction_pointer = self.d_instruction_pointers[opcode];
            self.setIndices(d_instruction_pointer);
            if max(self.indices) > len(self.cur_memory)-1:
                self.cur_memory = np.append(self.cur_memory, np.zeros(max(self.indices) - len(self.cur_memory) + 1, dtype='int64'), axis=0);
            if (opcode == 1):
                self.cur_memory[self.indices[2]] = sum(self.cur_memory[self.indices[:-1]]);
            elif (opcode == 2):
                self.cur_memory[self.indices[2]] = np.prod(self.cur_memory[self.indices[:-1]]);
            elif (opcode == 3):
                if (self.inputs_given == 0 and self.phase!= None):
                    self.cur_memory[self.indices[0]] = self.phase;
                else:
                    self.cur_memory[self.indices[0]] = self.input;
                self.inputs_given += 1;
            elif (opcode == 4):
                self.outputs.append(self.cur_memory[self.indices[0]]);
                if (breakatoutput):
                    self.instruction_pointer += d_instruction_pointer;
                    break;
            elif (opcode == 5):
                if (self.cur_memory[self.indices[0]]!=0):
                    d_instruction_pointer = self.cur_memory[self.indices[1]] - self.instruction_pointer;
            elif (opcode == 6):
                if (self.cur_memory[self.indices[0]]==0):
                    d_instruction_pointer = self.cur_memory[self.indices[1]] - self.instruction_pointer;
            elif (opcode == 7):
                if (self.cur_memory[self.indices[0]]<self.cur_memory[self.indices[1]]):
                    self.cur_memory[self.indices[2]] = 1;
                else:
                    self.cur_memory[self.indices[2]] = 0;
            elif (opcode == 8):
                if (self.cur_memory[self.indices[0]]==self.cur_memory[self.indices[1]]):
                    self.cur_memory[self.indices[2]] = 1;
                else:
                    self.cur_memory[self.indices[2]] = 0;
            elif (opcode == 9):
                self.relative_pointer += self.cur_memory[self.indices[0]];
            self.instruction_pointer += d_instruction_pointer;
        return self.cur_memory[0];
        
    def setIndices(self, length : int) -> type(None):
        opcode = self.cur_memory[self.instruction_pointer];
        for i in range(length-1):
            mode = opcode // 10**(i+2)%10;
            if (mode==2):
                self.indices[i] = (self.relative_pointer + self.cur_memory[self.instruction_pointer+1+i]);
            if (mode==1):
                self.indices[i] = (self.instruction_pointer+1+i)
            if (mode==0):
                self.indices[i] = (self.cur_memory[self.instruction_pointer+1+i])

    def reset(self) -> type(None):
        self.instruction_pointer = 0;
        self.relative_pointer = 0;
        self.inputs_given = 0;
        self.cur_memory = self.base_memory.copy()
    
    def checkComplete(self) -> bool:
        return self.cur_memory[self.instruction_pointer]%100 == 99;


#%%
if (__name__ == '__main__'):
    #Store in digits
    data = pd.read_csv('Input_Day9.txt', header=None).T;
    data.columns=['opcode']
    intcode = IntCode(data.values.T[0]);
    #intcode = IntCode(np.array([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]));
    #intcode = IntCode(np.array([1102,34915192,34915192,7,4,7,99,0], dtype='int64'));
    #intcode = IntCode(np.array([104,1125899906842624,99], dtype='int64'));
    
    
    
    intcode.execute(1);

        
        
    print("Day 9-1 answer is {0}".format(intcode.outputs[0]));
    t1 = time.time();
    intcode.reset()
    intcode.execute(2);
    
    print("Day 9-2 answer is {0}".format(intcode.outputs));


    
    #%%
    t2 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));
    print ("Programme took {0} seconds to run".format(t2-t1));