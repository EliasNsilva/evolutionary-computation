import random
import matplotlib.pyplot as plt

seq1 = 'ATCGAGCTAGCTAGC--'
seq2 = 'CTAGCTAGCT--CTCCCAA'
seq3 = 'GCTAG-TAGCTAGCTAG'
sequences = [seq1, seq2, seq3]

POPULATION_SIZE = 100
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1

# Função para avaliar a qualidade do alinhamento
def score_alignment(alignment):
    score = 0
    max_length = max([len(seq) for seq in alignment])
    for i in range(max_length):
        column = [row[i] for row in alignment if i < len(row)]
        for j in range(len(column)):
            for k in range(j+1, len(column)):
                if column[j] == '-' or column[k] == '-':
                    continue
                elif column[j] != column[k]:
                    score -= 1
                else:
                    score += 1
    return score

# Criação da população inicial: 50% de gaps para cada sequência e igualar o tamanho delas
def create_population():
    population = []
    for i in range(POPULATION_SIZE):
        max_length = max([len(seq) for seq in sequences])
        alignment = []
        for seq in sequences:
            gaps = '-' * ((max_length - len(seq)) + round(max_length / 2))
            seq = list(seq)
            for gap in gaps:
                seq.insert(random.randint(0, len(seq)), gap)
            alignment.append(seq)
        population.append(alignment)
    return population

# Crumzaento: escolher aleatoriamente um gene de cada pai
def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# Mutação: remover todos os gaps e inserir novos gaps aleatoriamente
def mutate(individual):
    mutated = []
    for seq in individual:
        if random.random() < MUTATION_RATE:
            seq = list(seq)
            length = len(seq)
            seq.remove('-')
            gaps = '-' * ((length - len(seq)))
            for gap in gaps:
                seq.insert(random.randint(0, len(seq)), gap)
            mutated.append(seq)
        else:
            mutated.append(seq)
    return mutated

# Seleção elitista: selecionar os 20% melhores indivíduos da população
def select(population):
    sorted_population = sorted(population, key=score_alignment, reverse=True)
    return sorted_population[:int(POPULATION_SIZE * 0.2)]

if __name__ == '__main__':
    # Criar uma população inicial aleatória
    population = create_population()
    best_score = []

    for generation in range(NUM_GENERATIONS):
        selected = select(population)
        # Criar uma nova população através do cruzamento dos indivíduos selecionados
        offspring = []
        while len(offspring) < POPULATION_SIZE:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            child = crossover(parent1, parent2)
            child = mutate(child)
            offspring.append(child)
        # Substituir a população anterior pela nova população
        population = offspring

        best_alignment = max(population, key=score_alignment)
        best_score.append(score_alignment(best_alignment))
    
    best_alignment = max(population, key=score_alignment)
    print('Melhor alinhamento:')
    for seq in best_alignment:
        print(seq)
    print(f'Melhor fitness = {score_alignment(best_alignment)}')
    plt.plot(range(NUM_GENERATIONS), best_score, color='green')
    plt.show()
