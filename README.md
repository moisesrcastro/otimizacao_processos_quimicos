# Processo de Produção do Tolueno

Todos os processos químicos e bioquímicos têm uma estrutura semelhante. O objetivo
é criar um produto mais valioso a partir de uma matéria-prima menos valioso enquanto
maximiza o lucro. A estrutura genérica do processo envolve cinco etapas: 
1. Preparação para alimentação do reator,
2. Reação, 
3. Preparação para alimentação do separador,
4. Separação e
5. Reciclo. 

Neste projeto, iremos analisar um processo genérico para determinar os parâmetros
de processo ótimos.

# Histórico do processo

O diagrama de fluxo do processo genérico é apresentado na Figura 1. A matéria-prima é A, mas a corrente de alimentação contém 20% (mols) de inertes, i (impurezas não reativas), a uma vazão total de 100 kmol/h e 50 °C. A corrente de alimentação é misturado com reciclado, que não reagiu e, em seguida, pré-aquecido a pelo menos 75 °C, mas não mais do que 150 °C antes de entrar no reator. A fonte de calor é vapor de baixa pressão a 160 °C que se condensa a
uma temperatura constante. No reator, a reação que ocorre é A→B, com uma conversão máxima possível de 95%. O reator é adiabático (o que significa que nenhum calor é adicionado ou removido), e pode-se supor que o aumento de temperatura é 50 °C. A corrente de saída do reator deve ser resfriada para 50 °C utilizando água de resfriamento (Cp = 4,184 kJ / kg °C) a qual entra a 30 °C e sai a 40 °C. O separador é considerado ideal (Não existe tal coisa na realidade!).  produto puro B é retirado na corrente 7, enquanto que todo o A vai para a corrente 8. Como todo reagente com elevado valor, A, é reciclado em vez de ser descartado (corrente 2). No entanto, desde que haja algum inerte, isto é, um componente que não reagiu, deve haver uma corrente de purga (Corrente 9), para evitar um aumento descontrolado no sistema. Vamos supor que todas as correntes de processamento têm as mesmas propriedades: &rho; = 900 kg/m3 e Cp = 2,1 kJ/kg °C. Os pesos moleculares de ambos os reagentes A e B são 100 kg/kmol e o peso molecular do inerte é de 50 kg/kmol. O calor de condensação/vaporização é de 2100 kJ/kg.

**Figura 1 –** Fluxograma de processo para produção de B.

![image](https://user-images.githubusercontent.com/93684961/226199156-ce2805d8-3883-44b1-8e59-241b509cd802.png)

# Dados para os cálculos dos custos de construção
A taxa de reação para esta reação, -r<sub>A</sub>, é dada em termos de concentração de reagente A (C<sub>A</sub>) por:

$$ −r_{A} = kC_{A} (2)$$

onde,

$$ k[s^{-1}]= {2,5 exp(3500 \over T[K])} (3)$$

e T é a temperatura média no reator T=(T <sub>Saída</sub> + T<sub>Entrada</sub>)/2. A equação para a concepção do
reator é dada por:
$$V = {v_{0}  X_{A} \over k  (1 - X_{A})} (4)$$

em que V é o volume do reator (m<sup>3</sup>), v<sub>0</sub> é a vazão volumétrica do fluido para dentro do reator
(m<sup>3</sup>/s), e X<sub>A</sub> é a conversão.

A equação de projeto para os trocadores de calor são dadas por:

$$ Q = m_{i}Cp_{i}(T_{OUT}−T_{IN}) = U A F \Delta T_{ln} (5)$$ 

para fluxos que passam por uma mudança de temperatura, ou para fluxos submetidos a uma mudança de fase (ou evaporação ou condensação):

$$ Q = m_{i}\Delta H_{vap} = U A F \Delta T_{ln} (6)$$

onde,

$$ \Delta T_{ln} =  {(T_{h,IN} - T_{c,OUT}) - (T_{h,OUT} - T_{c,IN}) \over ln[{T_{h,IN} - T_{c,OUT} \over T_{h,OUT} - T_{c,IN}}]} (7)$$ 

e 

F = 1,0 para E-201, F = 0,8 para E-202,

U = coeficiente global de transferência de calor = 1000 W / m<sup>2</sup>K

c, h = fria e corrente quente, respectivamente 

O custo de um permutador de calor com base na sua área, que pode ser calculada através da resolução para A em ambos os Equação 5 ou 6. A equação é custo:

$$ PC_{hx} = 12.000 A[m^2]^{0,57} (8)$$

O custo do reator pode ser estimada pela

$$ PC_{reactor}  = 20.000V[m^3]^{0,85} (9)$$

O custo do separador pode ser estimada pela

$$ PC_{tower}  = 2.000m[kg/h]^{0,65} (10)$$

# Dados para o cálculo dos custos operacionais

O custo da água de resfriamento é

$$ UC_{w} =  1,48^{10−5} (11)$$

e o custo de vapor é

$$ UC_{stm} = 13,00 (12)$$

A matéria-prima A (contendo I) é avaliado em US $ 0.50/kg, e o produto B é avaliada em $0,70/kg. Fluxo 9 é uma corrente de resíduos, e o seu destino deve ser considerada. Neste momento, não temos certeza de como este fluxo serão tratadas. Se ele pode ser queimado como combustível, o valor do combustível é

$$ UC_{burn} = 0,6 (13)$$

com base na quantidade de A no fluxo, uma vez que o inerte não irá queimar. Esta é uma receita. Se o efluente (A+I) tem de ser tratada, o custo é

$$ UC_{treat} = 0,036 (14)$$ 
