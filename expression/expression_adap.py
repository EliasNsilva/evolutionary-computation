import random


OPERATIONS = ['+', '-', '*', '/']

# Define o número máximo de níveis da árvore sintática
MAX_DEPTH = 3

POPULATION_SIZE = 100

MAX_GENERATIONS = 10000

TARGET_VALUE = 124

class Expression():
    def __init__(self, operator, right_value, left_value):
        self.operator = operator
        self.left_value = left_value
        self.right_value = right_value
    def __str__(self):
        return f' ({self.left_value} {self.operator} {self.right_value}) '

# calcula o valor de uma árvore sintática
def evaluate(expression):
    if isinstance(expression, int):
        return expression
    else:
        left_value = evaluate(expression.left_value)
        right_value = evaluate(expression.right_value)
        operator = expression.operator
        if operator == '+':
            return left_value + right_value
        elif operator == '-':
            return left_value - right_value
        elif operator == '*':
            return left_value * right_value
        elif operator == '/':
            if right_value == 0:
                return left_value
            else:
                return left_value / right_value

def create_expression(depth):
    if depth == 0:
        return random.randint(1, 10)
    else:
        operator = random.choice(OPERATIONS)
        left_expression = create_expression(depth - 1)
        right_expression = create_expression(depth - 1)
        return Expression(operator, left_expression, right_expression)

def generate_population(size):
    population = []
    for i in range(size):
        expression = create_expression(MAX_DEPTH)
        population.append(expression)
    return population

def fitness(expression):
    value = evaluate(expression)
    error = abs(TARGET_VALUE - value)
    return 1.0 / (error + 1)

def select_parents(population):
    fitnesses = list(map(fitness, population))
    total_fitness = sum(fitnesses)
    probabilities = list(map(lambda fitness: fitness / total_fitness, fitnesses))
    parent1 = random.choices(population, weights=probabilities)[0]
    parent2 = random.choices(population, weights=probabilities)[0]

    return parent1, parent2

# calculo de diversidade da população
def diversity(population):
    diversity = 0
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            if population[i] == population[j]:
                diversity += 1
    return diversity

def crossover(parent1, parent2, crossover_rate):
    if isinstance(parent1, int) or isinstance(parent2, int):
        return random.randint(1, 10)
    else:
        if random.uniform(0, 1) < crossover_rate:
            operator = random.choice([parent1.operator, parent2.operator])
            left_expression = crossover(parent1.left_value, parent2.left_value, crossover_rate)
            right_expression = crossover(parent1.right_value, parent2.right_value, crossover_rate)
            return Expression(operator, left_expression, right_expression)
        else:
            return random.choice([parent1, parent2])

def mutate(expression, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        return create_expression(MAX_DEPTH)
    elif isinstance(expression, int):
        return expression
    else:
        operator = expression.operator
        left_expression = mutate(expression.left_value, mutation_rate)
        right_expression = mutate(expression.right_value, mutation_rate)
        return Expression(operator, left_expression, right_expression)
    
def genetic_algorithm_adap(crossover_rate, mutation_rate):
    population = generate_population(POPULATION_SIZE)
    max_fitness = []
    for i in range(MAX_GENERATIONS):
        parent1, parent2 = select_parents(population)

        population_diversity = diversity(population)

        if population_diversity >= POPULATION_SIZE * 0.7:
            crossover_rate = crossover_rate + (crossover_rate * 0.1)
            mutation_rate = mutation_rate - (mutation_rate * 0.1)
        else:
            crossover_rate = crossover_rate - (crossover_rate * 0.1)
            mutation_rate = mutation_rate + (mutation_rate * 0.1)

        child = crossover(parent1, parent2, crossover_rate)

        child = mutate(child, mutation_rate)

        child_fitness = fitness(child)
        max_fitness.append(child_fitness)

        if child_fitness == 1:
            return child, max_fitness

        population = sorted(population, key=fitness)
        population[0] = child

    population = sorted(population, key=fitness, reverse=True)
    return population[0], max_fitness

# best_expression, max_fitness = genetic_algorithm_adap(0.8, 0.1)

# print("Melhor expressão encontrada: ", best_expression)
# print("Valor da expressão: ", evaluate(best_expression))


