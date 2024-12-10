from sat import Sat
import random
import math
import matplotlib.pyplot as plt
import seaborn
import pandas


initial_temperature = 2 # substitua pelo valor desejado
alpha = 0.001  # taxa de resfriamento.
beta = 1 # controla a velocidade com que a temperatura diminui
bitflip = 5
sa_max = 5
solucoes = []
removal = 1
class Anneling:
    def __init__(self, file, len) -> None:
        self.sat = Sat(file, len) # sat class
        self.sat.upload()
        self.temp = initial_temperature
        self.current_solution = []
        self.neighbor_solution = []

        self.current_value = 0
        self.neighbor_value = 0
        self.solucao=0

        self.interation_number = 0
        self.fatorResfriamento = 4 # 4.5 # min 1 max 5, 4 funciona ok

        # to graphics generator
        self.temperaturas = []
        self.graphic_solution = []

    def generate_initial_solution(self):
        for i in range(0,self.sat.get_quant_var()):
            bit = random.randint(0, 1)
            self.current_solution.append(bit)
            self.neighbor_solution.append(bit)
    
        self.current_value = self.sat.fitness(self.current_solution)[0]
        
        self.neighbor_value  = self.current_value


    def generate_neighbor(self,bitflipquant):
        quant_bitflip = random.randint(0, bitflipquant)
        self.neighbor_solution = []
        for i in self.current_solution:
            self.neighbor_solution.append(i)
        
        for i in range(0,quant_bitflip):
            cases_to_flip = random.sample(range(0, self.sat.get_quant_var()), quant_bitflip)
            for case in cases_to_flip:
                if self.neighbor_solution[case] == 0:
                    self.neighbor_solution[case] = 1
                else:
                    self.neighbor_solution[case] = 0

        self.neighbor_value = self.sat.fitness(self.neighbor_solution)[0]

    

    def sigmoid_cooling(self,initial_temperature, alpha, beta, t):
        # self.temp = initial_temperature / (1 + alpha * math.log(1 + t / beta))
        self.temp = pow((1-(t/250000)), 10)
        self.temperaturas.append(self.temp)
        

    def interation(self, max, bitflip):
        for i in range(0, max): 
            self.graphic_solution.append(100-self.current_value)
            self.interation_number = i
            if self.current_value == 100:
                self.graphic_solution.append(100-self.current_value)
                self.solucao = self.sat.fitness(self.current_solution)[1]

                solucoes.append(self.sat.quant_clausulas-self.solucao)
                
                return self.current_value
            
            if i % sa_max:
                self.sigmoid_cooling(initial_temperature, alpha, beta, i)

            if i == 70000:
                bitflip = bitflip - removal
            if i == 140000:
                bitflip = bitflip - removal
            if i == 170000:
                bitflip = bitflip - removal

            self.generate_neighbor(bitflip)

            if self.current_value <= self.neighbor_value:
                self.current_solution = []
                for j in self.neighbor_solution:  
                    self.current_solution.append(j)

                self.current_value = self.neighbor_value         
            else:
                probability = math.exp(-(self.current_value - self.neighbor_value) / self.temp)

                if random.uniform(0, 1) < probability:
                    self.current_solution = []
                    for j in self.neighbor_solution:  
                        self.current_solution.append(j)

                    self.current_value = self.neighbor_value
            self.solucao = self.sat.fitness(self.current_solution)[1]

        solucoes.append(self.sat.quant_clausulas-self.solucao)
        return self.current_value
    

    def plot_queda_temp(self,name_save, var):
        plt.clf()
        plt.cla()
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
        axs[0].plot(self.graphic_solution)
        axs[0].set_title(f'Gráfico convergencia')
        axs[0].set_xlabel('Iterações')
        axs[0].set_ylabel('% Clausulas não resolvidas')
        axs[1].plot(self.temperaturas)
        axs[1].set_title('Queda Temperatura')
        axs[1].set_xlabel('Iterações')
        axs[1].set_ylabel('Temperatura')
        plt.savefig(f'{name_save}_SA.png')


    def save_info(self, file):
        file = open(file,'a')
        file.write(f'{solucoes}-{self.current_value} - {self.interation_number} - {self.current_solution}\n')
        file.close()

for i in range(0,10):
    a = Anneling('20.txt', 3)
    a.generate_initial_solution()
    a.generate_neighbor(bitflip)
    a.interation(250000,bitflip)
    pack_name = f'interaction{i+1}'
    a.plot_queda_temp(pack_name,100)
    a.save_info('solution_20.txt')

plt.clf()
plt.cla()
plt.boxplot(solucoes)
plt.savefig('bloxplot_SA.png')
# df_solucoes = pandas.DataFrame(solucoes)
# seaborn.boxplot(data=df_solucoes)print
