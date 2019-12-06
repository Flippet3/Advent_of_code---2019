import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DiagnosticProgram:
    
    def __init__(self, memory : np.ndarray) -> type(None):
        self.base_memory = memory;
        self.reset();
    
    def execute(self, i_input : int) -> int:
        self.input = i_input;
        self.outputs = [];
        while True:
            opcode = self.cur_memory[self.instruction_pointer]%100;
            if (opcode == 1):
                d_instruction_pointer = 4;
                indices = self.getIndices(d_instruction_pointer);
                self.cur_memory[indices[-1]] = sum(self.cur_memory[indices[:-1]]);
            elif (opcode == 2):
                d_instruction_pointer = 4;
                indices = self.getIndices(d_instruction_pointer);
                self.cur_memory[indices[-1]] = np.prod(self.cur_memory[indices[:-1]]);
            elif (opcode == 3):
                d_instruction_pointer = 2;
                indices = self.getIndices(d_instruction_pointer);
                self.cur_memory[indices[0]] = self.input;
            elif (opcode == 4):
                d_instruction_pointer = 2;
                indices = self.getIndices(d_instruction_pointer);
                self.outputs.append(self.cur_memory[indices[0]]);
            elif (opcode == 5):
                d_instruction_pointer = 3;
                indices = self.getIndices(d_instruction_pointer);
                if (self.cur_memory[indices[0]]!=0):
                    d_instruction_pointer = self.cur_memory[indices[1]] - self.instruction_pointer;
            elif (opcode == 6):
                d_instruction_pointer = 3;
                indices = self.getIndices(d_instruction_pointer);
                if (self.cur_memory[indices[0]]==0):
                    d_instruction_pointer = self.cur_memory[indices[1]] - self.instruction_pointer;
            elif (opcode == 7):
                d_instruction_pointer = 4;
                indices = self.getIndices(d_instruction_pointer);
                if (self.cur_memory[indices[0]]<self.cur_memory[indices[1]]):
                    self.cur_memory[indices[2]] = 1;
                else:
                    self.cur_memory[indices[2]] = 0;
            elif (opcode == 8):
                d_instruction_pointer = 4;
                indices = self.getIndices(d_instruction_pointer);
                if (self.cur_memory[indices[0]]==self.cur_memory[indices[1]]):
                    self.cur_memory[indices[2]] = 1;
                else:
                    self.cur_memory[indices[2]] = 0;
            elif(opcode == 99):
                break;
            self.instruction_pointer += d_instruction_pointer;
        return self.cur_memory[0];
        
    def getIndices(self, length : int) -> list:
        values = []
        opcode = self.cur_memory[self.instruction_pointer];
        for i in range(length-1):
            mode = int((opcode * 10**(-i-2))%10);
            if (mode==1):
                values.append(self.instruction_pointer+1+i)
            if (mode==0):
                values.append(self.cur_memory[self.instruction_pointer+1+i])
        return values;

    def reset(self) -> type(None):
        self.instruction_pointer = 0;
        self.cur_memory = self.base_memory.copy()


#%%
if (__name__ == '__main__'):
    #Store in digits
    data = pd.read_csv('Input_Day5.txt', header=None).T;
    data.columns=['opcode']
    dp = DiagnosticProgram(data.opcode.values);
    #dp = DiagnosticProgram(np.array([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]));
    

    dp.execute(1)
    print("Day 5-1 answer is {0}".format(dp.outputs[-1]));
    
    dp.reset()
    dp.execute(5)
    print("Day 5-2 answer is {0}".format(dp.outputs[-1]));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));