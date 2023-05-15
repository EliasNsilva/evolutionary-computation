import random
import numpy as np

MAX_VOICE_GSM   = 125
MAX_VOICE_WCDMA = 150
MAX_DATA_GSM    = 30
MAX_DATA_WCDMA  = 80
MAX_SUM_VOICE   = MAX_VOICE_GSM + MAX_VOICE_WCDMA # 275
MAX_SUM_DATA    = MAX_DATA_GSM + MAX_DATA_WCDMA  # 110
NUM_SERVICES    = 4 # 2 voice services and 2 data services (for each technology, gsm and wcdma)
MUTATION_RATE   = 0.1
# NET_CAPACITY = (MAX_VOICE_GSM, MAX_VOICE_WCDMA, MAX_DATA_GSM, MAX_DATA_WCDMA)

def generate_idv(n, start, end):
    return [random.uniform(start, end) for _ in range(n)]

def evaluate(population):
    fitnesses = []

    for chromo in population:
        voice_gsm, voice_wcdma, data_gsm, data_wcdma = chromo
        sum_voice = voice_gsm + voice_wcdma
        sum_data = data_gsm + data_wcdma

        if voice_gsm > MAX_VOICE_GSM or voice_wcdma > MAX_VOICE_WCDMA or data_gsm > MAX_DATA_GSM or data_wcdma > MAX_DATA_WCDMA:
            fitnesses.append(np.Infinity)
        elif sum_voice > MAX_SUM_VOICE or sum_data > MAX_SUM_DATA:
            fitnesses.append(np.Infinity)
        else:
            cost_gsm = np.power(-30 + data_gsm + 0.24 * voice_gsm, 2)
            cost_wcdma = np.power(-80 + data_wcdma + 0.53 * voice_wcdma, 2)
            sum_voice = 1 - (sum_voice/MAX_SUM_VOICE)
            sum_data = 1 - (sum_data/MAX_SUM_DATA)

            fitnesses.append((cost_gsm + cost_wcdma) * sum_data * sum_voice)

    return fitnesses

def select(fitnesses):
    ordered_idx = np.argsort(fitnesses)
    # dad_idx = int(NUM_SERVICES/2)
    # mom_idx = dad_idx-1
    return ordered_idx[0], ordered_idx[1]

def crossover(mom, dad):
    cross_pt = int(NUM_SERVICES/2)
    child1 = np.concatenate((mom[:cross_pt], dad[cross_pt:]))
    child2 = np.concatenate((dad[:cross_pt], mom[cross_pt:]))

    return child1, child2

def mutate(child):
    pos = np.random.randint(0, NUM_SERVICES, 1)
    op = np.random.choice([0,1]) # 0=sum, 1=subtract
    mutated_child = child.copy()
    if not op:
        mutated_child[pos] = (child[pos]*(1+MUTATION_RATE))
    else:
        mutated_child[pos] = (child[pos]*(1-MUTATION_RATE))

    return mutated_child

def print_output(idv, score):
    print(f'~ best individual found ~\n{idv}    -- cost {score}\n')


def start_ga(pop_size=4, mutation_rate=MUTATION_RATE, generations=50):
    population = [generate_idv(NUM_SERVICES, 0.0, 150.0) for _ in range(pop_size)]
    # population = [[50,82.50,24.96,36], [64,121.88,5,15], [38,80.63,24.48,37],[44,69,24.96,31]]
    best_idv, best_score = None, np.inf

    for _ in range(generations):
        new_generation = []
        fitnesses = evaluate(population)
        mom_idx, dad_idx = select(fitnesses)

        if fitnesses[mom_idx] < best_score:
            best_idv = population[mom_idx]
            best_score = fitnesses[mom_idx]
        # print(best_idv, best_score)

        # if best_score <= 0.0:
        #     break

        child1, child2 = crossover(population[mom_idx], population[dad_idx])

        if np.random.uniform() <= mutation_rate:
            child1 = mutate(child1)
            child2 = mutate(child2)

        new_generation.extend([population[mom_idx], population[dad_idx], child1, child2])
        population = new_generation

    print(best_idv, best_score)

if __name__ == '__main__':
    start_ga()