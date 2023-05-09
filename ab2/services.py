import numpy as np
import random

# Definindo os limites máximos de usuários por tecnologia e tipo de serviço
max_voice_gsm = 150
max_data_gsm = 80
max_voice_wcdma = 275
max_data_wcdma = 110

# Gerando uma população aleatória de 4 indivíduos com 4 genes cada
population_size = 4
genes_per_individual = 4
taxa_variacao_mutacao=0.1
taxa_mutacao_populacao=0.2
population = np.random.rand(population_size, genes_per_individual)

percentual_prox_gen =0.5
geracoes = 50

# Multiplicando cada valor de gene pelo limite máximo correspondente
population[:,0] *= max_voice_gsm    # Voz GSM
population[:,1] *= max_data_gsm    # Dados GSM
population[:,2] *= max_voice_wcdma # Voz WCDMA
population[:,3] *= max_data_wcdma  # Dados WCDMA

print("População: ", population)

def cruzamento(pai, mae):
    ponto_corte = int(genes_per_individual/2)
    filho1 = np.concatenate((pai[:ponto_corte],mae[ponto_corte:]))
    filho2 = np.concatenate((mae[:ponto_corte],pai[ponto_corte:]))

    return filho1, filho2

def mutacao(cromo):
    pos=np.random.randint(0, genes_per_individual, 1)
    op=np.random.choice([0,1]) # 0=soma, 1=subtracao
    if not op:
        cromo[pos] = cromo[pos]*(1+taxa_variacao_mutacao)
        print(cromo)
    else:
        cromo[pos] = cromo[pos]*(1-taxa_variacao_mutacao)
        print(cromo)
    return cromo

def calcular_custo(populacao):
    custos = []
    for cromossomo in populacao:
        # Descompacta o cromossomo em quatro genes
        voz_gsm, dados_gsm, voz_wcdma, dados_wcdma = cromossomo
        # Calcula a distribuição de usuários de voz e dados em cada tecnologia
        voz_gsm_total = voz_gsm + 0.5*dados_gsm # cada usuário de dados consome o dobro de um de voz
        dados_gsm_total = dados_gsm
        voz_wcdma_total = voz_wcdma + 0.5*dados_wcdma # cada usuário de dados consome o dobro de um de voz
        dados_wcdma_total = dados_wcdma
        
        # Verifica se a capacidade máxima de usuários de voz e dados foi excedida
        if voz_gsm_total > 150 or dados_gsm_total > 80:
            custos.append(float("inf")) # Penaliza o cromossomo com um custo muito alto
        elif voz_wcdma_total > 275 or dados_wcdma_total > 110:
            custos.append(float("inf")) # Penaliza o cromossomo com um custo muito alto
        else:
            # Calcula o custo como a diferença entre a demanda desejada e a distribuição obtida
            custo = ((0.4 - voz_gsm_total/150)**2 +
                     (0.2 - dados_gsm_total/80)**2 +
                     (0.3 - voz_wcdma_total/275)**2 +
                     (0.1 - dados_wcdma_total/110)**2)
            custos.append(custo)
    return custos


custo = calcular_custo(population)

def encontrar_melhor_individuo(populacao):
    custos = calcular_custo(populacao)
    melhor_individuo = populacao[np.argmin(custos)]
    return melhor_individuo


#Função com o tam da população correta
def selecionar_individuos(populacao, custos, n):
    # Calcular valores de aptidão
    aptidoes = [1/c for c in custos]
    # Normalizar aptidões
    soma_aptidoes = sum(aptidoes)
    aptidoes = [a/soma_aptidoes for a in aptidoes]
    
    # Selecionar os N indivíduos com menor custo
    indices_menores_custos = np.argsort(custos)[:int(n)]
    mantidos = [populacao[i] for i in indices_menores_custos]
    
    # Selecionar indivíduos substitutos utilizando o método da roleta
    substitutos = []
    
    for i in range(len(populacao) - int(n)):
        aleatorio = random.random()
        soma = 0
        for j, aptidao in enumerate(aptidoes):
            soma += aptidao

            if soma > aleatorio:
                # Adicionar o cromossomo com menor custo entre os escolhidos
                if np.array_equal(population[j], mantidos):
                    menor_custo = float("inf")
                    melhor_cromossomo = None
                    for k in range(len(populacao)):
                        if populacao[k] not in mantidos and custos[k] < menor_custo:
                            menor_custo = custos[k]
                            melhor_cromossomo = populacao[k]
                    substitutos.append(melhor_cromossomo)
                else:
                    substitutos.append(populacao[j])
                break
    
    # Retornar indivíduos mantidos e substitutos
    return mantidos + substitutos


menor = encontrar_melhor_individuo(population)
media_aritimetica =  np.mean(menor)
nova_geracao = selecionar_individuos(population, custo, percentual_prox_gen*genes_per_individual)

print("Custo do cromossomo aleatório: ", custo)
print("Custo do menor cromossomo aleatório: ", menor )
print("Média aritimética: ", media_aritimetica)
print("Nova geração: ", nova_geracao)
