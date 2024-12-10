from sat import Sat
import random
import math
import matplotlib.pyplot as plt

solucoes = []

class Randon_Search:
    def __init__(self, file, len) -> None:
        self.sat = Sat(file, len) # sat class
        self.sat.upload()

        self.current_solution = []
        self.neighbor_solution = []
        self.solucao=0

        self.current_value = 0
        self.neighbor_value = 0

        # to graphics generator
        self.graphic_solution = []

    def generate_initial_solution(self):
        for i in range(0,self.sat.get_quant_var()):
            bit = random.randint(0, 1)
            self.current_solution.append(bit)
            self.neighbor_solution.append(bit)
        
        self.current_value = self.sat.fitness(self.current_solution)[0]
        self.neighbor_value  = self.current_value


    def randon_solution(self):
        self.neighbor_solution = []
        for i in self.current_solution:
            self.neighbor_solution.append(random.randint(0, 1))
        self.neighbor_value = self.sat.fitness(self.neighbor_solution)[0]
        self.graphic_solution.append(100-self.neighbor_value)

    def interation(self,quant):
        aux = 0
        for i in range(0,quant):
            self.randon_solution()
            if self.current_value < self.neighbor_value:
                aux =i
                self.current_solution = []
                for i in self.neighbor_solution:
                    self.current_solution.append(i)
                self.current_value = self.neighbor_value

        self.solucao = self.sat.fitness(self.current_solution)[1]
        solucoes.append(self.sat.quant_clausulas-self.solucao)
            
    
        return (aux, self.current_value)
    

    def plot_queda_temp(self,name_save,var):
        plt.clf()
        plt.cla()
    
        plt.plot(self.graphic_solution)
        plt.title(f'Random search {var} Variaveis ')
        plt.xlabel('Iterações')
        plt.ylabel('% Sat NOT Solved')
        plt.savefig(f'{name_save}_RS.png')

    def save_info(self, file):
        file = open(file,'a')
        file.write(f'{solucoes}- {self.current_value} - {self.current_solution}\n')
        file.close()


if __name__=='__main__':
   for i in range(0, 10):
        a = Randon_Search('250.txt', 3)
        a.generate_initial_solution()
        a.interation(250000)
        pack_name = f'interaction{i+1}_random'
        a.plot_queda_temp(pack_name,20)
        a.save_info('20_random.txt')