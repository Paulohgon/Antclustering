
import pygame
import random
import datetime
import math

linhas = 70
colunas = 70
matrix_folhas = [[0 for _ in range(colunas)] for _ in range(linhas)]


class Dados:
    def __init__(self, matrix):
        self.carregada_por = None
        self.carregada = False
        self.populado = False
        self.valorx = 0
        self.valory = 0
        while not self.populado:
            self.x = random.randint(0, linhas-1)
            self.y = random.randint(0, colunas-1)
            if matrix[self.x][self.y] == 0:
                self.populado = True
                matrix[self.x][self.y] = self


folhas = [Dados(matrix_folhas)for _ in range(10)]

for i in matrix_folhas:
    for j in i:
        if type(j) == Dados:
            print(type(j))
            print(Dados)