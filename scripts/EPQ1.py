import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

def Otimizacao(parametros, sign = -1, op = 1):

    p_reciclo = parametros[0]
    Xa = parametros[1]
    T = parametros[2]

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
    PC_TC_2 = 12000 * (A_TC_2 ** 0.57)

    '''Reator'''
    PC_R = 20000 * (Vol ** 0.85)

    '''Torre de Separação'''
    m6 = (cA_6 * MA) + (cB_6 * MB) + (cI_6 * MI)
    PC_T = 2000 * (m6 ** 0.65)

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

    '''Considerando a combustão'''
    m9 = cA_9 * MA
    Combust = m9 * ano * 0.6

    '''Considerando o tratamento da corrente 9'''
    Tratamento = (m9 + cI_9 * MI) * ano * 0.036

    if op == 1:
        Receita = Product + Combust

    if op == 2:
        Receita = Product - Tratamento

    EAOC = sign * (Receita - EAOC_op)

    return EAOC

a = (0.1, 0.98)
b = (0.1, 0.95)
c = (75, 150)

bound = (a, b, c)

Params = minimize(Otimizacao, [0.81, 0.95, 150], method='SLSQP', bounds=bound) #op = 1
#Params = minimize(Otimizacao, [0.7, 0.9, 150], method='SLSQP', bounds=bound) #op = 2

if __name__ == '__main__':
    print(f'EAOC = {round((-1) * Params.fun, 2)}[$/ano]')
EAOC_otm = Params.fun * (-1)
part = Params.x[0]
Xa = Params.x[1]
Temp = Params.x[2]

if __name__ == '__main__':
    print(f'Partição de reciclo = {round(part, 4)}\n'
        f'Conversão = {round(Xa, 4)}\n'
        f'Temperatura = {round(Temp, 2)}ºC')

'''Superfice de controle 1 - Fixando o valor da partição de reciclo'''
xa = np.linspace(0.1, 0.95, 50)
T = np.linspace(75, 150, 50)
p = part
EAOCi = []
X, T = np.meshgrid(xa, T)

for i in range(len(xa)):

    EAOCi.append((-1) * Otimizacao([p, X[i], T[i]]))

'''Superficie de controle 2  - Fixando o valor da conversão'''
x = Xa
pr = np.linspace(0.1, 0.98, 50)
T = np.linspace(75, 150, 50)
EAOCj = []
P, T = np.meshgrid(pr, T)

for i in range(len(xa)):

    EAOCj.append((-1) * Otimizacao([P[i], x, T[i]]))

if __name__ == "__main__":
    '''Plotando as superficies de resposta'''
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(Xa, Temp, EAOC_otm, color='black')
    ax1.contour3D(X, T, EAOCi, 1000, cmap="viridis")
    ax1.set_title(f'Partição de reciclo = {round(part, 3)}')
    ax1.set_xlabel('Conversão')
    ax1.set_ylabel('Temperatura')
    ax1.set_zlabel('EAOC')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.contour3D(P, T, EAOCj, 1000, cmap="viridis")
    ax2.scatter(p, Temp, EAOC_otm, color='black')
    ax2.set_title(f'Conversão = {round(x, 3)}')
    ax2.set_xlabel('Partição de reciclo')
    ax2.set_ylabel('Temperatura')
    ax2.set_zlabel('EAOC')
    plt.show()
