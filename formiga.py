

import pygame
import random
import math
gridDisplay = pygame.display.set_mode((700, 700))
color = (255, 0, 0)
gridDisplay.fill(color)
linhas = 70
colunas = 70

matrix = [[0 for _ in range(colunas)] for _ in range(linhas)]

grid_node_width = 10
grid_node_height = 10

tamanho_formiga_alt = 10
tamanho_formiga_lng = 10


class Formiga:
    def __init__(self, x, y, matrix):
        self.populado = False
        self.carregando = False
        self.aoredor = 0
        while not self.populado:
            self.x = random.randint(0, linhas-1)
            self.y = random.randint(0, colunas-1)
            if matrix[self.x][self.y] == 0:
                matrix[self.x][self.y] = 1
                self.populado = True


class Folha:
    def __init__(self, matrix):
        self.carregada_por = None
        self.carregada = False
        self.populado = False
        while not self.populado:
            self.x = random.randint(0, linhas-1)
            self.y = random.randint(0, colunas-1)
            if matrix[self.x][self.y] == 0:
                matrix[self.x][self.y] = 2
                self.populado = True


folhas = [Folha(matrix) for _ in range(70)]
formigas = [Formiga(1, 2, matrix) for _ in range(10)]


def createSquare(x, y, color):
    pygame.draw.rect(gridDisplay, color, [
                     x, y, grid_node_width, grid_node_height])


def get_element(matriz, linha, coluna):
    return matriz[linha % linhas][coluna % colunas]


def decide_pegar(formiga, matrix):
    chance = (1 - formiga.aoredor / 8.0)
    if random.uniform(0, 1) < chance and not formiga.carregando:
        formiga.carregando = True
        matrix[formiga.x][formiga.y] = 1
        for folha in folhas:
            if folha.x == formiga.x and folha.y == formiga.y:
                print("alo")
                folha.carregada_por = formiga
                folha.carregada = True


def decide_largar(formiga, matrix):
    # chance = formiga.aoredor / 7.9
    chance = math.exp(formiga.aoredor)
    print(chance)
    if random.uniform(0, 6) < chance and formiga.carregando:
        formiga.carregando = False
        matrix[formiga.x][formiga.y] = 2

        for folha in folhas:
            if folha.carregada_por == formiga:
                folha.carregada = False
                folha.carregada_por = None
                folha.x = formiga.x
                folha.y = formiga.y


def get_visao(formiga, matrix):
    formiga.aoredor = 0
    proximo = get_element(matrix, formiga.x-1, formiga.y)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x+1, formiga.y)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x, formiga.y-1)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x, formiga.y+1)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x+1, formiga.y+1)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x-1, formiga.y-1)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x-1, formiga.y+1)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x+1, formiga.y-1)
    if proximo == 2:
        formiga.aoredor = formiga.aoredor+1


def atualiza_folhas(folhas, matrix):
    for folha in folhas:
        if matrix[folha.x][folha.y] == 0 and not folha.carregada:
            matrix[folha.x][folha.y] = 2


def move_outra_ponta(formiga, matrix, direcao):
    if formiga.x == 0 and direcao == 1:
        if matrix[linhas-1][formiga.y] == 0:
            matrix[formiga.x][formiga.y] = 0
            formiga.x = linhas-1
            matrix[formiga.x][formiga.y] = 1

    if formiga.x == linhas-1 and direcao == 2:
        if matrix[0][formiga.y] == 0:
            matrix[formiga.x][formiga.y] = 0
            formiga.x = 0
            matrix[formiga.x][formiga.y] = 1
    if formiga.y == 0 and direcao == 3:
        if matrix[formiga.x][colunas-1] == 0:
            matrix[formiga.x][formiga.y] = 0
            formiga.y = colunas-1
            matrix[formiga.x][formiga.y] = 1
    if formiga.y == colunas-1 and direcao == 4:
        if matrix[formiga.x][colunas-1] == 0:
            matrix[formiga.x][0] = 0
            formiga.y = 0
            matrix[formiga.x][formiga.y] = 1


def move(formigas, matrix):
    cont = 0
    for formiga in formigas:
        direcao = random.randint(1, 4)
        if direcao == 1:
            if formiga.x == 0:

                move_outra_ponta(formiga, matrix, direcao)
                get_visao(formiga, matrix)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x-1][formiga.y] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.x = formiga.x - 1
                    matrix[formiga.x][formiga.y] = 1
                    get_visao(formiga, matrix)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        if direcao == 2:
            if formiga.x == linhas-1:

                move_outra_ponta(formiga, matrix, direcao)
                get_visao(formiga, matrix)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x+1][formiga.y] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.x = formiga.x + 1
                    matrix[formiga.x][formiga.y] = 1
                    get_visao(formiga, matrix)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        if direcao == 3:
            if formiga.y == 0:

                move_outra_ponta(formiga, matrix, direcao)
                get_visao(formiga, matrix)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x][formiga.y-1] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.y = formiga.y - 1
                    matrix[formiga.x][formiga.y] = 1
                    get_visao(formiga, matrix)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        if direcao == 4:
            if formiga.y == colunas-1:
                move_outra_ponta(formiga, matrix, direcao)
                get_visao(formiga, matrix)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x][formiga.y+1] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.y = formiga.y + 1
                    matrix[formiga.x][formiga.y] = 1
                    get_visao(formiga, matrix)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        cont = cont+1
        atualiza_folhas(folhas, matrix)

    visualizeGrid()


def visualizeGrid():
    y = 0
    for row in matrix:
        x = 0  # for every row we start at the left of the screen again
        for item in row:
            if item == 0:
                createSquare(x, y, (255, 255, 255))
            if item == 1:
                createSquare(x, y, (0, 0, 0))
            if item == 2:
                createSquare(x, y, (0, 255, 0))
            # for ever item/number in that row we move one "step" to the right
            x += grid_node_width
        y += grid_node_width   # for every new row we move one "step" downwards
    pygame.display.update()


while True:
    visualizeGrid()  # call the function
    move(formigas, matrix)
