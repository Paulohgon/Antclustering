import random
import matplotlib.pyplot as plt
import math

class Sat:
    def __init__(self,file, len):
        self.quant_var = None
        self.clause_length = len
        self.file = file
        self.instances =[]
        self.quant_clausulas = 0

    def get_quant_var(self):
        return self.quant_var
    
    def get_clause_length(self):
        return self.clause_length
  

    def upload(self):
        file = open(self.file,'r')
        file = file.read()
        file = file.split('\n')
        for line in file:
            line = line.split(' ')
            if line[0]== 'p':
                self.quant_var = int(line[2])
                self.quant_clausulas = int(line[3])
            else:
                instance =[]
                for i in range(0, self.clause_length):
                    instance.append(int(line[i]))
                self.instances.append(instance)


    def fitness(self, solution): # if param = 0 fitness of solution if param = 1 solution of neighbor
        count = 0
        for instance in self.instances:
            instace_conditional = False
            for var in instance:
                if var > 0:
                    if solution[var-1] == 1:
                        instace_conditional  = True
                        break
                else:
                    if solution[(var*(-1))-1] == 0:
                        instace_conditional  = True
                        break

            if instace_conditional:
                count +=1

        return ((count/self.quant_clausulas)*100,count)