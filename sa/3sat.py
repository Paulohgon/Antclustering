import random
import math
import matplotlib.pyplot as plt
import numpy as np


NUM_VARIAVEIS = 0
NUM_CLAUSULAS = 0
# 3CNF-SAT
pegaNumVari = 1
pegaNumClau = 1
comecaClausula = 1
terminaClausula = 0
variaveisValoradas = []
clausulas = []
clausulasValoradas = []
expressaoBool = []
listaResultados = []


def is_number(inputString):
    return any(char.isdigit() for char in inputString)


# with open("/content/drive/MyDrive/3cnf/uf250-01.cnf","r") as file:
with open("20.txt", "r") as file:

    for line in file:
        if (not line.startswith('c')):
            if (line.startswith('p')):  # Setando as variaveis globais
                for word in line.split():
                    if (is_number(word) and pegaNumVari == 1):
                        NUM_VARIAVEIS = word
                        pegaNumVari = 0
                    elif (is_number(word) and pegaNumClau == 1):
                        NUM_CLAUSULAS = word
                        pegaNumClau = 0

            else:  # Leitura das Clausulas
                aux = []
                for p in line.split():
                    if p != '0' and is_number(p):
                        aux.append(p)
                if len(aux) != 0:
                    clausulas.append(aux)

for i in range(int(NUM_VARIAVEIS)):
    variaveisValoradas.append(random.randint(0, 1))


for i in range(int(NUM_CLAUSULAS)):
    aux = []
    for j in range(len(clausulas[i])):
        if (int(clausulas[i][j]) < 0):
            aux.append(not variaveisValoradas[(int(clausulas[i][j])*-1) - 1])
        elif (int(clausulas[i][j]) > 0):
            aux.append(not not variaveisValoradas[int(clausulas[i][j])-1])
    if len(aux) != 0:
        clausulasValoradas.append(aux)

for i in clausulasValoradas:
    if any(j == True for j in i):
        expressaoBool.append(True)
    else:
        expressaoBool.append(False)


def numFalse(expressao):
    numFalse = 0
    for f in expressao:
        if f == False:
            numFalse = numFalse + 1
    return numFalse


print(variaveisValoradas)


###### SIMULATED ANNEALING ######
numFalso = numFalse(expressaoBool)
melhorNumFalso = numFalso
melhorSolucao = variaveisValoradas
temperatura = 1
tempInicial = temperatura
tempFinal = 0.000001
listaTemp = []
listaFalsos = []
interMaxTotal = 250000
interTempTotal = 0
mudancaMaxVizinho = 1  # int(math.sqrt(int(NUM_VARIAVEIS)))

for i in range(interMaxTotal):
    interTempTotal = interTempTotal + 1
    # print(interTemp)
    numBitFlip = random.randint(1, mudancaMaxVizinho)
    vizinho = [x for x in variaveisValoradas]
    for i in range(numBitFlip):
        qualMuda = random.randint(0, int(NUM_VARIAVEIS)-1)
        if vizinho[qualMuda] == False:
            vizinho[qualMuda] = 1
        else:
            vizinho[qualMuda] = 0

    exprBool = []
    clauValo = []
    for i in range(int(NUM_CLAUSULAS)):
        aux = []
        for j in range(len(clausulas[i])):
            if (int(clausulas[i][j]) < 0):
                aux.append(not vizinho[(int(clausulas[i][j])*-1) - 1])
            elif (int(clausulas[i][j]) > 0):
                aux.append(not not vizinho[int(clausulas[i][j])-1])
        if len(aux) != 0:
            clauValo.append(aux)

    for i in clauValo:
        if any(j == True for j in i):
            exprBool.append(True)
        else:
            exprBool.append(False)
    falsos = numFalse(exprBool)
    if falsos == 0:
        melhorSolucao = vizinho.copy()
        break
    delta = falsos - numFalso
    if falsos < numFalso:
        variaveisValoradas = vizinho.copy()
        listaFalsos.append(falsos)
        numFalso = falsos
        if falsos < melhorNumFalso:
            melhorSolucao = variaveisValoradas.copy()
            melhorNumFalso = falsos
    else:
        x = random.random()
        probab = temperatura/2
        if x < probab:
            listaFalsos.append(falsos)
            variaveisValoradas = vizinho.copy()
            numFalso = falsos

    listaTemp.append(temperatura)
    temperatura = pow((1-(interTempTotal/interMaxTotal)), 10)
    # print(f'T: {temperatura}')
    # print(f'C: {numFalso}')
    # print(f'B: {melhorNumFalso}')

print(melhorSolucao)
expBool = []
cl = []
for i in range(int(NUM_CLAUSULAS)):
    aux = []
    for j in range(len(clausulas[i])):
        if (int(clausulas[i][j]) < 0):
            aux.append(not melhorSolucao[(int(clausulas[i][j])*-1) - 1])
        elif (int(clausulas[i][j]) > 0):
            aux.append(not not melhorSolucao[int(clausulas[i][j])-1])
    if len(aux) != 0:
        cl.append(aux)

for i in cl:
    if any(j == True for j in i):
        expBool.append(True)
    else:
        expBool.append(False)
res = numFalse(expBool)
print(res)




plt.subplot(2, 1, 1)
plt.title("Temperatura")
plt.plot(listaTemp)


plt.subplot(2, 1, 2)
plt.title("SA")
plt.ylabel("Número de falsos")
plt.plot(listaFalsos)
plt.show()
