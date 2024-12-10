import random
import math
import numpy as np 

bias = 0.5
compr_sepala = 5.1
larg_sepala=3.5
compr_petala=1.4
larg_petala=0.2

# compr_sepala = 6.4
# larg_sepala=3.1
# compr_petala=5.5
# larg_petala=1.8




def soma(x,y,w,z):
    p1=random.random()
    p2=random.random()
    p3=random.random()
    p4=random.random()
    soma = x*p1+y*p2+w*p3+z*p4
    return soma

def ativacao_sigmoid(c_sepala,l_sepala,c_petala,l_petala):
    soma_val = soma(c_sepala,l_sepala,c_petala,l_petala)
    sig = 1 / (1 + math.exp(-soma_val))
    return sig


def ativacao_relu(c_sepala,l_sepala,c_petala,l_petala):
    soma_val = soma(c_sepala,l_sepala,c_petala,l_petala)
    relu = soma_val if soma_val > 0 else 0
    return relu

def ativacao_step(c_sepala,l_sepala,c_petala,l_petala):
    soma_val = soma(c_sepala,l_sepala,c_petala,l_petala)
    step = 1 if soma_val >= 0 else 0
    return step

relu = ativacao_relu(compr_sepala,larg_sepala,compr_petala,larg_petala)
sigmoid = ativacao_sigmoid(compr_sepala,larg_sepala,compr_petala,larg_petala)
step = ativacao_step(compr_sepala,larg_sepala,compr_petala,larg_petala)


print("relu",relu)
print("sig",sigmoid)
print("step",step)