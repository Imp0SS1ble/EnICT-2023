import matplotlib.pyplot as plt  # Importando a biblioteca matplotlib.pyplot e dando o apelido de plt para a plotagem do gráfico.
from scipy.optimize import curve_fit  # Importando a biblioteca scipy.optimize para o ajuste de curva e cálculo dos parâmetros fixos da curva.
import numpy as np  # Importando a biblioteca numpy e dando o apelido de np, que possui várias funcionalidades matemáticas.
from sklearn.metrics import r2_score  # Importando a biblioteca sklearn.metrics para calcular o R².
import sys  # Importando a biblioteca sys, que permite o uso da funcionalidade sys.exit(0).

m = []  # Declarando o vetor que armazenará os dados de massa.
F = []  # Declarando o vetor que armazenará os dados de força.
x = []  # Declarando o vetor que armazenará os dados de elongação da mola.
F_ajustado = []  # Declarando o vetor que armazenará os dados calculados de força da mola a partir dos dados de parâmetros fixos na equação y.
g = 9.81  # Valor utilizado como aceleração gravitacional (Fundamentos de Física: Mecânica. v. 1)

N = int(input('Quantas molas foram utilizadas? '))  # Pedindo para o usuário informar quantas molas foram usadas.

if N != 1:  # Se o valor for diferente de 1, então:
    associação_de_molas = int(input('Informe a associação das molas (1 para série ou 2 para paralelo): '))  # Pedindo para o usuário informar qual a associação das molas usadas.
else:  # Se o número de molas for igual a um ou não for positivo, então:
    print('Valor inválido! Reinicie o código e digite um valor válido.')  # Avisa o usuário que o valor informado não é válido e pede para reiniciar o código.
    sys.exit(0)  # Se essa linha for compilada, finaliza-se a execução do código aqui.

n = int(input('Quantas massas diferentes foram utilizadas? '))  # Pedindo para o usuário informar quantos valores de massas foram usados.

for i in range(0, n):  # Loop até coletar a quantidade informada pelo usuário.
    m.append(float(input('Informe a ' + str(i+1) + 'ª massa utilizada (em quilogramas): ')))  # Pedindo para o usuário informar as massas utilizadas.
    F.append(m[i] * g)  # Calculando a força peso que será igual à força elástica, no caso da massa estar pendurada na perpendicular.
    x.append(float(input('Qual foi a deformação da mola (em metros) com a ' + str(i+1) + 'ª massa: ')))  # Pedindo para o usuário informar a elongação na(s) mola(s) ocasionada pela massa adicionada.

def y(x, K, a):  # Criando a função com a equação da lei de Hooke com x em módulo e adicionado o termo 'a' para uma linha de tendência mais precisa.
    return x * K + a

fig, ax = plt.subplots(figsize=(8, 5))  # Definindo o tamanho do gráfico para melhor visualização.
xData = np.array(x)  # Colocando as variáveis de elongação nos dados do eixo x.
yData = np.array(F)  # Colocando as variáveis de força nos dados do eixo y.
plt.axis(ymin=0, ymax=(F[n-1]) * 1.1, xmin=0, xmax=(x[n-1]) * 1.1)  # Definindo os valores limites dos eixos do gráfico.

if N == 1:  # Se há apenas uma mola, o título do gráfico será o texto entre aspas simples a seguir:
    plt.title('Força elástica: Lei de Hooke (Com uma mola)')
elif associação_de_molas == 1:  # Se há associação em série de molas, o título do gráfico será o texto entre aspas simples a seguir:
    plt.title('Força elástica: Lei de Hooke (Associação em série de molas)')
else:  # Se há associação em paralelo de molas, o título do gráfico será o texto entre aspas simples a seguir:
    plt.title('Força elástica: Lei de Hooke (Associação em paralelo de molas)')

plt.plot(xData, yData, 'bo', label='Dados')  # Plotando valores informados pelo usuário.
popt, pcov = curve_fit(y, xData, yData)  # Calculando parâmetros fixos por meio da função da linha 28 e 29.
xFit = np.arange(0.0, x[n-1], 0.000001)  # Definindo o tamanho e o intervalo da curva de tendência.

for i in range(0, n):  # As linhas 47 e 48 serão responsáveis pelo cálculo da força com os dados dos parâmetros fixos calculados e inseridos na equação y.
    F_ajustado.append(x[i] * popt[0] + popt[1])

r2 = r2_score(F_ajustado, F)  # A partir dos dados de massa que se calcula a força medidos pelo usuário, compara-se estatisticamente com a força obtida pelos parâmetros fixos estimados pelo script, obtendo-se o R², onde 1 representa uma compatibilidade perfeita entre dados experimentais e os estimados, já 0 representa uma incompatibilidade total entre eles.

if N == 1:  # Se só se utilizou uma mola, há apenas uma constante elástica, portanto, se utiliza K.
    plt.plot(xFit, y(xFit, *popt), 'r', label=f'Parâmetro de ajuste: K=%5.5f N/m, a=%5.5f N\nEquação: F = x*K + a\nR² = {r2:.5f}' % tuple(popt))  # Plotando valores calculados no ajuste de curva.
else:  # Se utilizou uma associação de molas, há uma constante elástica equivalente, portanto, se utiliza K_eq.
    plt.plot(xFit, y(xFit, *popt), 'r', label=f'Parâmetro de ajuste: K_eq.=%5.5f N/m, a=%5.5f N\nEquação: F = x*K_eq. + a\nR² = {r2:.5f}' % tuple(popt)) # Plotando valores calculados no ajuste de curva.

plt.xlabel('x (m)') # Título da eixo x.
plt.ylabel('F (N)') # Título da eixo y.
plt.legend() # Exibição da legenda.
plt.show() # Exibição do gráfico.