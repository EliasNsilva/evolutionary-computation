from expression_adap import genetic_algorithm_adap
from expression_evo import genetic_algorithm
import matplotlib.pyplot as plt

if __name__ == "__main__":
    crossover_rate = 0.8
    mutation_rate = 0.1
    best_expression_adap, max_fitness_adap = genetic_algorithm_adap(crossover_rate, mutation_rate)
    best_expression, max_fitness = genetic_algorithm(crossover_rate, mutation_rate)
    print("Melhor expressão sem adaptação", best_expression)
    print("Melhor expressão com adaptação", best_expression_adap)
    # print("Fitness sem adaptação", max_fitness)
    # print("Fitness com adaptação", max_fitness_adap)
    
    plt.plot(max_fitness, max_fitness, color='blue', label='Sem adaptação')
    plt.plot(max_fitness_adap, max_fitness_adap, color='red', label='Com adaptação')
    plt.legend()
    plt.show()
