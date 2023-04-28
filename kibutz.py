import numpy as np
from scipy.optimize import minimize

# Solicitar o tamanho da área irrigável de cada kibutz
area_irrigavel_k1 = float(input("Digite o tamanho da área irrigável do kibutz 1: "))
area_irrigavel_k2 = float(input("Digite o tamanho da área irrigável do kibutz 2: "))
area_irrigavel_k3 = float(input("Digite o tamanho da área irrigável do kibutz 3: "))

#Solucitar a quantidade máxima de área que pode ser dedicada a cada plantação
max_beterraba = float(input("Digite a quantidade máxima de área que pode ser dedicada à beterraba: "))
max_algodao = float(input("Digite a quantidade máxima de área que pode ser dedicada ao algodão: "))
max_sorgo = float(input("Digite a quantidade máxima de área que pode ser dedicada ao sorgo: "))

#Solicitar a quantidade de água alocada para a irrigação de cada kibutz
agua_k1 = float(input("Digite a quantidade de água alocada para a irrigação do kibutz 1: "))
agua_k2 = float(input("Digite a quantidade de água alocada para a irrigação do kibutz 2: "))
agua_k3 = float(input("Digite a quantidade de água alocada para a irrigação do kibutz 3: "))

#Solicitar os retornos líquidos esperados para cada plantação
retorno_beterraba = float(input("Digite o retorno líquido esperado para a beterraba: "))
retorno_algodao = float(input("Digite o retorno líquido esperado para o algodão: "))
retorno_sorgo = float(input("Digite o retorno líquido esperado para o sorgo: "))

#Definindo a função objetivo
def objetivo(x):
    return -1 * np.sum([
        retorno_beterraba * (x[0] + x[3] + x[6]),
        retorno_algodao * (x[1] + x[4] + x[7]),
        retorno_sorgo * (x[2] + x[5] + x[8])
    ])

#Restrições
#Área máxima que pode ser dedicada a cada plantação
restricoes = [
    {"type": "ineq", "fun": lambda x: max_beterraba - np.sum(x[::3])},
    {"type": "ineq", "fun": lambda x: max_algodao - np.sum(x[1::3])},
    {"type": "ineq", "fun": lambda x: max_sorgo - np.sum(x[2::3])}
]
#Vetor de áreas irrigáveis de cada kibutz
area_irrigavel = np.array([area_irrigavel_k1, area_irrigavel_k2, area_irrigavel_k3])

#Vetor de quantidades máximas de área que pode ser dedicada a cada plantação
max_area_plantacao = np.array([max_beterraba, max_algodao, max_sorgo])

#Vetor de quantidades de água alocadas para a irrigação de cada kibutz
agua_alocada = np.array([agua_k1, agua_k2, agua_k3])

#Vetor de retornos líquidos esperados para cada plantação, em milhares de dólares.
retorno_plantacao = np.array([retorno_beterraba, retorno_algodao, retorno_sorgo])

#Vetor de variáveis de decisão iniciais (acres a serem dedicados a cada plantação nos kibutzim)
x0 = np.zeros(9)

#Função para as restrições
def restricoes_fun(x):
    return np.array([
        max_area_plantacao - np.array([np.sum(x[::3]), np.sum(x[1::3]), np.sum(x[2::3])]),
        np.sum(x.reshape((3, 3)), axis=0) - area_irrigavel,
        np.sum(x.reshape((3, 3)) * retorno_plantacao, axis=0) - agua_alocada
    ])

# Solução do problema de otimização
solucao = minimize(objetivo, x0, constraints=restricoes, method='SLSQP')

#Quantidades de acres a serem dedicados a cada plantação nos kibutzim
quantidades_acres = solucao.x.reshape((3, 3))

#Retorno líquido total
retorno_total = -1 * solucao.fun

print("\nQuantidades de acres a serem dedicados a cada plantação nos kibutzim:")
print(quantidades_acres)
print("\nRetorno líquido total:", retorno_total)
