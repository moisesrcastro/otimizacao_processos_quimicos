import numpy as np
from scipy.optimize import fsolve, minimize
from EPQ1 import Xa, EAOC_otm, part, Temp
import matplotlib.pyplot as plt


def Precificacao(params):
    preco = params[0]
    Xa = params[1]
    p_reciclo = params[2]
    T = params[3]

    '''Informações do Sistema'''
    Tc_1 = 50;          Th_1 = 160;
    Twc_IN = 30;        Twc_OUT = 40;
    Cp_w = 4.184;       Cp_c = 2.1;
    ro = 900;
    MA = 100;           MB = 100;
    MI = 50;
    F1 = 1;             F2 = 0.8;
    U = 3600;
    ano = 8000
    n = 12
    i = 0.11
    Ts_tc2 = 50

    '''Os balanços materiais dependem da conversão e da partição do reciclo'''
    #Calculo das correntes do processo em Kmol / h

    cA_1 = 80
    cB_1 = 0
    cI_1 = 20

    cA_2 = cA_1 * p_reciclo * (1 - Xa)/(1 - p_reciclo + p_reciclo * Xa)
    cB_2 = 0
    cI_2 = cI_1 * p_reciclo / (1 - p_reciclo)

    cA_3 = cA_1 + cA_2
    cB_3 = cB_1 + cB_2
    cI_3 = cI_1 + cI_2

    cA_4 = cA_3
    cB_4 = cB_3
    cI_4 = cI_3

    cA_5 = cA_3 * (1 - Xa)
    cB_5 = cA_3 * Xa
    cI_5 = cI_3

    cA_6 = cA_5
    cB_6 = cB_5
    cI_6 = cI_5

    cA_7 = 0
    cB_7 = cB_5
    cI_7 = 0

    cA_8 = cA_5
    cB_8 = 0
    cI_8 = cI_5

    cA_9 = cA_8 * (1 - p_reciclo)
    cB_9 = 0
    cI_9 = cI_8 * (1 - p_reciclo)

    '''Trocador de calor 1'''
    m3 = (cA_3 * MA) + (cB_3 * MB) + (cI_3 * MI)
    Q_TC_1 = m3 * Cp_c * (T - Tc_1)
    delta_T_ln1 = ((Th_1 - T)-(Th_1 - Tc_1))/np.log((Th_1 - T)/(Th_1 - Tc_1))

    '''Aréa do Trocador de Calor E - 201'''
    A_TC_1 = Q_TC_1 / (U * F1 * delta_T_ln1)

    '''Reator'''
    Tr = (T + 25) + 273.15
    K = 3600 * 2.5 * np.exp(-3500/Tr)
    m4 = (cA_4 * MA) + (cB_4 * MB) + (cI_4 * MI)
    v0 = m4 / ro

    '''Volume do Reator R - 201'''
    Vol = v0 * Xa / (K * (1 - Xa))

    '''Trocador de calor 2'''
    m5 = (cA_5 * MA) + (cB_5 * MB) + (cI_5 * MI)
    Q_TC_2 = m5 * Cp_c * ((T + 50) - Ts_tc2)
    delta_T_ln2 = (((T + 50) - Twc_OUT) - (Ts_tc2 - Twc_IN)) / np.log(((T + 50) - Twc_OUT) / (Ts_tc2 - Twc_IN))

    '''Aréa do Trocador de Calor E - 202'''
    A_TC_2 = Q_TC_2 / (U * F2 * delta_T_ln2)

    '''Custos'''

    '''Trocadores de Calor'''
    PC_TC_1 = 12000 * (A_TC_1 ** 0.57)
    PC_TC_2 = 12000 * (A_TC_2 ** 0.57)#

    '''Reator'''
    PC_R = 20000 * (Vol ** 0.85)#

    '''Torre de Separação'''
    m6 = (cA_6 * MA) + (cB_6 * MB) + (cI_6 * MI)
    PC_T = 2000 * (m6 ** 0.65)#

    '''Utilidades'''
    Q12 = Q_TC_1 * ano / (10 ** 6)
    P_Vapor = 13 * Q12

    ma = ano * (Q_TC_2 /(Cp_w * (Twc_IN - Twc_OUT)))
    P_Agua = 1.48 * (10 ** (-5)) * ma

    '''Matéria - Prima'''
    m1 = cA_1 * MA + cI_1 * MI
    P_Mat = m1 * 0.5 * ano

    '''Custos Operacionais'''
    PC = PC_R + PC_T + PC_TC_1 + PC_TC_2
    taxa = i * ((i + 1) ** n) / (((i + 1) ** n) - 1)
    UC = P_Agua + P_Vapor + P_Mat

    EAOC_op = PC * taxa + UC

    '''Receita'''
    m7 = cB_7 * MB
    Product = m7 * ano * 0.7

    '''Considerando a venda da corrente 9'''
    Venda = (cA_9 * MA + cI_9 * MI) * ano * preco
    Receita = Product + Venda

    EAOC = Receita - EAOC_op

    return EAOC

def Restricao(params):
    preco = params[0]
    Xa = params[1]
    p_reciclo = params[2]
    T = params[3]
    EAOC = Precificacao([preco, Xa, p_reciclo, T])

    return EAOC - EAOC_otm

'''Preço de venda da corrente 9'''

a = (0.025, 0.25) #preço
b = (0.1, 0.95) #conversão
c = (0.1, 0.98) #reciclo
d = (75, 150) #temperatura
con1 = {'type':'eq', 'fun':Restricao}
cons = [(con1)]
bound = (a, b, c, d)

preco = minimize(Precificacao, [0.04, 0.95, 0.81, 120], method='SLSQP', bounds=bound, constraints=cons)

print(f'Preço = ${round(preco.x[0], 5)}/Kg\n'
      f'Partição de reciclo = {round(preco.x[2], 2)}\n'
      f'Conversão = {round(preco.x[1], 2)}\n'
      f'Temperatura = {round(preco.x[3], 3)}ºC\n'
      f'EAOC = {preco.fun}')
EAOC_otm = preco.fun
valor = preco.x[0]
Xa = preco.x[1]
p = preco.x[2]
T = preco.x[3]

