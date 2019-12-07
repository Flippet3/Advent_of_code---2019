import time
t0 = time.time();

# Day 1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations


class IntCode:
    def __init__(self, memory : np.ndarray) -> type(None):
        self.base_memory = memory;
        self.reset();
    
    def execute(self, i_input : int, i_phase : int = None, breakatoutput : bool = False) -> int:
        self.input = i_input;
        self.phase = i_phase;
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
                if (self.inputs_given == 0 and self.phase!= None):
                    self.cur_memory[indices[0]] = self.phase;
                else:
                    self.cur_memory[indices[0]] = self.input;
                self.inputs_given += 1;
            elif (opcode == 4):
                d_instruction_pointer = 2;
                indices = self.getIndices(d_instruction_pointer);
                self.outputs.append(self.cur_memory[indices[0]]);
                if (breakatoutput):
                    self.instruction_pointer += d_instruction_pointer;
                    break;
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
        self.inputs_given = 0;
        self.cur_memory = self.base_memory.copy()
    
    def checkComplete(self) -> bool:
        return self.cur_memory[self.instruction_pointer]%100 == 99;


#%%
if (__name__ == '__main__'):
    #Store in digits
    data = pd.read_csv('Input_Day7.txt', header=None).T;
    data.columns=['opcode']
    amplifiers = []
    for i in range(5):
        amplifiers.append(IntCode(data.opcode.values));
        #amplifiers.append(IntCode(np.array([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])));
    
    perms = set([''.join(p) for p in permutations('01234')]);
    
    outputs = len(perms) * [0];
    for i,phase in enumerate(perms):
        output = 0;
        for j in range(len(phase)):
            amplifiers[j].execute(output, int(phase[j]));
            output = amplifiers[j].outputs[-1];
            amplifiers[j].reset();
        outputs[i] = output;
        
        
    print("Day 7-1 answer is {0}".format(max(outputs)));
    
    perms2 = set([''.join(p) for p in permutations('56789')]);
    
    outputs2 = len(perms) * [0];
    for i,phase in enumerate(perms2):
        output = 0;
        halted = False;
        while not halted:
            for j in range(len(phase)):
                amplifiers[j].execute(output, int(phase[j]), True);
                if len(amplifiers[j].outputs) > 0:
                    output = amplifiers[j].outputs[-1];
                if j == len(phase)-1:
                    if amplifiers[j].checkComplete():
                        halted=True;
        outputs2[i] = output;
        for j in range(len(phase)):
            amplifiers[j].reset();
        
        
        
    
    print("Day 7-2 answer is {0}".format(max(outputs2)));


    
    #%%
    t1 = time.time();
    print ("Programme took {0} seconds to run".format(t1-t0));