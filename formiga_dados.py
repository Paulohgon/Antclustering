

import pygame
import random
import datetime
import math
gridDisplay = pygame.display.set_mode((600, 600))
color = (255, 0, 0)
gridDisplay.fill(color)
linhas = 60
colunas =60
alpha = 2
s = 3
k1= 0.40
k2=0.60
matrix = [[0 for _ in range(colunas)] for _ in range(linhas)]
matrix_folhas = [[0 for _ in range(colunas)] for _ in range(linhas)]

grid_node_width = 10
grid_node_height = 10

tamanho_formiga_alt = 10
tamanho_formiga_lng = 10


class Formiga:
    def __init__(self, x, y, matrix):
        self.populado = False
        self.carregando = False
        self.aoredor = 0
        self.carregando_dado = None
        while not self.populado:
            self.x = random.randint(0, linhas-1)
            self.y = random.randint(0, colunas-1)
            if matrix[self.x][self.y] == 0:
                self.populado = True
                matrix[self.x][self.y] = self


class Dados:
    def __init__(self, matrix,valorx,valory,tag):
        self.carregada_por = None
        self.carregada = False
        self.populado = False
        self.valorx = valorx
        self.valory = valory
        self.tag = tag
        while not self.populado:
            self.x = random.randint(0, linhas-1)
            self.y = random.randint(0, colunas-1)
            if matrix[self.x][self.y] == 0:
                self.populado = True
                matrix[self.x][self.y] = self


folhas = []
arquivo = open("dados.txt", "r")
for x in arquivo:
    dados_txt = x.split("/")
    dado1 = Dados(matrix_folhas, float(dados_txt[0]), float(dados_txt[1]), int(dados_txt[2]))
    folhas.append(dado1)
formigas = [Formiga(1, 2, matrix) for _ in range(25)]


def createSquare(x, y, color):
    pygame.draw.rect(gridDisplay, color, [
                     x, y, grid_node_width, grid_node_height])


def get_element(matriz, linha, coluna):
    return matriz[linha % linhas][coluna % colunas]


def similaridade_dados(matrix, formiga):
    visao = get_visao(formiga, matrix_folhas)
    
    dado_carregado = formiga.carregando_dado
    dado_local = matrix_folhas[formiga.x][formiga.y]
    soma_distancias = 0
    for elemento in visao:

        elemento_da_soma = 0

        if dado_carregado:
            elemento_da_soma = (1-(math.sqrt((dado_carregado.valorx-elemento.valorx)**2 + (dado_carregado.valory-elemento.valory)**2))/alpha)

        elif dado_local != 0:
            elemento_da_soma = (1-(math.sqrt((dado_local.valorx-elemento.valorx)**2 + (dado_local.valory-elemento.valory)**2))/alpha)

        soma_distancias = soma_distancias + elemento_da_soma

    similaridade = soma_distancias/(9)
    if similaridade > 0:
        # print(similaridade)
        return similaridade
    else:
        return 0


def decide_pegar(formiga, matrix):
    if not formiga.carregando and (matrix_folhas[formiga.x][formiga.y]) != 0:
        fx = similaridade_dados(matrix, formiga)
        chance = (k1/(k1+fx))**2
        if random.uniform(0, 1) <= chance:
            formiga.carregando = True
            matrix_folhas[formiga.x][formiga.y] = 0
            for folha in folhas:
                if folha.x == formiga.x and folha.y == formiga.y:
                    folha.carregada_por = formiga
                    folha.carregada = True
                    formiga.carregando_dado = folha


def decide_largar(formiga, matrix):
    # chance = formiga.aoredor / 7.7
    if formiga.carregando and (matrix_folhas[formiga.x][formiga.y]) == 0:
        fx = similaridade_dados(matrix, formiga)
        chance = (fx/(k2+fx))**2

        if random.uniform(0, 1) <= chance:
            formiga.carregando = False
            matrix_folhas[formiga.x][formiga.y] = formiga.carregando_dado

            for folha in folhas:
                if folha.carregada_por == formiga:
                    folha.carregada = False
                    folha.carregada_por = None
                    formiga.carregando_dado = None
                    folha.x = formiga.x
                    folha.y = formiga.y


def get_visao(formiga, matrix):
    lista_proximos = []
    formiga.aoredor = 0
    proximo = get_element(matrix, formiga.x-1, formiga.y)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x+1, formiga.y)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x, formiga.y-1)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x, formiga.y+1)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x+1, formiga.y+1)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x-1, formiga.y-1)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x-1, formiga.y+1)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    proximo = get_element(matrix, formiga.x+1, formiga.y-1)
    if proximo != 0:
        lista_proximos.append(proximo)
        formiga.aoredor = formiga.aoredor+1
    return lista_proximos

def atualiza_folhas(folhas, matrix):
    for folha in folhas:
        if matrix[folha.x][folha.y] == 0 and not folha.carregada:
            matrix[folha.x][folha.y] = folha


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

        if get_element(matrix, formiga.x, 0) == 0:
            matrix[formiga.x][formiga.y] = 0
            formiga.y = 0
            matrix[formiga.x][formiga.y] = 1


def move(formigas, matrix):
    cont = 0
    for formiga in formigas:
        direcao = random.randint(1, 4)
        if direcao == 1:
            if formiga.x == 0:

                move_outra_ponta(formiga, matrix, direcao)
                # get_visao(formiga, matrix_folhas)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x-1][formiga.y] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.x = formiga.x - 1
                    matrix[formiga.x][formiga.y] = 1
                    # get_visao(formiga, matrix_folhas)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        if direcao == 2:
            if formiga.x == linhas-1:

                move_outra_ponta(formiga, matrix, direcao)
                # get_visao(formiga, matrix_folhas)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x+1][formiga.y] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.x = formiga.x + 1
                    matrix[formiga.x][formiga.y] = 1
                    # get_visao(formiga, matrix_folhas)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        if direcao == 3:
            if formiga.y == 0:

                move_outra_ponta(formiga, matrix, direcao)
                # get_visao(formiga, matrix_folhas)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x][formiga.y-1] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.y = formiga.y - 1
                    matrix[formiga.x][formiga.y] = 1
                    # get_visao(formiga, matrix_folhas)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        if direcao == 4:
            if formiga.y == colunas-1:
                move_outra_ponta(formiga, matrix, direcao)
                # get_visao(formiga, matrix_folhas)
                decide_pegar(formiga, matrix)
                decide_largar(formiga, matrix)

            else:
                if matrix[formiga.x][formiga.y+1] != 1:
                    matrix[formiga.x][formiga.y] = 0
                    formiga.y = formiga.y + 1
                    matrix[formiga.x][formiga.y] = 1
                    # get_visao(formiga, matrix_folhas)
                    decide_pegar(formiga, matrix)
                    decide_largar(formiga, matrix)

        cont = cont+1
        # atualiza_folhas(folhas, matrix)



def visualizeGrid():
    y = 0

    colum_len = 0
    for row in matrix:
        x = 0  # for every row we start at the left of the screen again
        row_len = 0
        for item in row:
            
            if item == 0:
                createSquare(x, y, (255, 255, 255))
            if item == 1:
                createSquare(x, y, (0, 0, 0))
            # if matrix_folhas[row_len][colum_len] == 2:
            #     createSquare(x, y, (0, 255, 0))
            # for ever item/number in that row we move one "step" to the right
            x += grid_node_width
            row_len = row_len+1
        # colum_len = colum_len+1
        y += grid_node_width   # for every new row we move one "step" downwards
    pygame.display.update()
    
    y = 0
    for linha_f in matrix_folhas:
        x = 0
        for folha in linha_f:
              
            if type(folha) == Dados:
                if folha.tag == 1:
                    createSquare(x, y, (0, 255, 0))
                if folha.tag == 2:
                    createSquare(x, y, (255, 255, 0))
                if folha.tag == 3:
                    createSquare(x, y, (0, 255, 255))
                if folha.tag == 4:
                    createSquare(x, y, (255, 0, 0))
                if folha.tag == 5:
                    createSquare(x, y, (0, 0, 255))
                if folha.tag == 6:
                    createSquare(x, y, (255, 0, 255))
                if folha.tag == 7:
                    createSquare(x, y, (120, 120, 50))
                if folha.tag == 8:
                    createSquare(x, y, (120, 0, 120))
                if folha.tag == 9:
                    createSquare(x, y, (0, 120, 120))
                if folha.tag == 10:
                    createSquare(x, y, (120, 50, 255))
                if folha.tag == 11:
                    createSquare(x, y, (50, 120, 255))
                if folha.tag == 12:
                    createSquare(x, y, (50, 255, 120))
                if folha.tag == 13:
                    createSquare(x, y, (255, 120, 50))
                if folha.tag == 14:
                    createSquare(x, y, (255, 50, 120))
                if folha.tag == 14:
                    createSquare(x, y, (120, 50, 155))
            x += grid_node_width

        y += grid_node_width
    pygame.display.update()

aux = 0
contf = 0
while aux < 4500000:
    random.seed(str(datetime.datetime.now()))
    move(formigas, matrix)
    aux = aux + 1
    # print(aux)
    # visualizeGrid()  # call the function
# while True:
    visualizeGrid()
