from expression_adap import genetic_algorithm_adap
from expression_evo import genetic_algorithm
from expression_adap_crom import genetic_algorithm_adap_crom
import matplotlib.pyplot as plt

if __name__ == "__main__":
    max_generations = 3000
    crossover_rate = 0.8
    mutation_rate = 0.1
    
    best_expression, best_value, max_fitness = genetic_algorithm(max_generations, crossover_rate, mutation_rate)
    best_expression_adap, best_value_adap, max_fitness_adap = genetic_algorithm_adap(max_generations, crossover_rate, mutation_rate)
    best_expression_adap_crom, best_value_adap_crom, max_fitness_adap_crom = genetic_algorithm_adap_crom(max_generations, crossover_rate, mutation_rate)

    print(f'Melhor expressão sem adaptação: {best_expression} = {best_value}\n')
    print(f'Melhor expressão com adaptação: {best_expression_adap} = {best_value_adap}\n')
    print(f'Melhor expressão com taxas em cada cromossomo: {best_expression_adap_crom} = {best_value_adap_crom}\n')
    
    # plt.plot(range(len(max_fitness)), max_fitness, color='blue', label='Sem adaptação')
    # plt.plot(range(len(max_fitness_adap)), max_fitness_adap, color='red', label='Com adaptação')
    # plt.plot(range(len(max_fitness_adap_crom)), max_fitness_adap_crom, color='green', label='Com taxas em cada cromosso')
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

    ax1.plot(range(len(max_fitness)), max_fitness, color='blue', label='Sem adaptação')
    ax1.set_title('Sem adaptação')
    ax1.set_ylabel('Fitness')

    ax2.plot(range(len(max_fitness_adap)), max_fitness_adap, color='red', label='Com adaptação')
    ax2.set_title('Com adaptação')
    ax2.set_ylabel('Fitness')

    ax3.plot(range(len(max_fitness_adap_crom)), max_fitness_adap_crom, color='green', label='Com taxas em cada cromossomo')
    ax3.set_title('Com taxas em cada cromossomo')
    ax3.set_ylabel('Fitness')
    ax3.set_xlabel('Gerações')
    
    plt.show()
