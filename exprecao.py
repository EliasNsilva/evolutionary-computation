import random

# Define as operações suportadas pela árvore sintática
OPERATIONS = ['+', '-', '*', '/']

# Define o número máximo de níveis da árvore sintática
MAX_DEPTH = 4

# Define o tamanho da população
POPULATION_SIZE = 100

# Define o número máximo de gerações
MAX_GENERATIONS = 100

# Define o valor que se deseja alcançar
TARGET_VALUE = 10

# Define a função que calcula o valor de uma árvore sintática
def evaluate(expression):
    if isinstance(expression, int):
        return expression
    else:
        left_value = evaluate(expression[1])
        right_value = evaluate(expression[2])
        operator = expression[0]
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

# Define a função que cria uma árvore sintática aleatória
def create_expression(depth):
    if depth == 0:
        return random.randint(1, 10)
    else:
        operator = random.choice(OPERATIONS)
        left_expression = create_expression(depth - 1)
        right_expression = create_expression(depth - 1)
        return [operator, left_expression, right_expression]

# Define a função que gera uma nova população
def generate_population(size):
    population = []
    for i in range(size):
        expression = create_expression(MAX_DEPTH)
        population.append(expression)
    return population

# Define a função que avalia a aptidão de uma árvore sintática
def fitness(expression):
    value = evaluate(expression)
    error = abs(TARGET_VALUE - value)
    return 1.0 / (error + 1)

# Define a função que seleciona dois pais para o cruzamento
def select_parents(population):
    fitnesses = [fitness(expression) for expression in population]
    total_fitness = sum(fitnesses)
    probabilities = [fitness / total_fitness for fitness in fitnesses]
    parent1 = random.choices(population, weights=probabilities)[0]
    parent2 = random.choices(population, weights=probabilities)[0]
    return parent1, parent2

# Define a função que realiza o cruzamento entre dois pais
def crossover(parent1, parent2):
    if isinstance(parent1, int) or isinstance(parent2, int):
        return random.randint(1, 10)
    else:
        operator = random.choice([parent1[0], parent2[0]])
        left_expression = crossover(parent1[1], parent2[1])
        right_expression = crossover(parent1[2], parent2[2])
        return [operator, left_expression, right_expression]

# Define a função que realiza a mutação em uma árvore sintática
def mutate(expression, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        return create_expression(MAX_DEPTH)
    elif isinstance(expression, int):
        return expression
    else:
        operator = expression[0]
        left_expression = mutate(expression[1], mutation_rate)
        right_expression = mutate(expression[2], mutation_rate)
        return [operator, left_expression, right_expression]
    
def genetic_algorithm():
    # Gera a população inicial
    population = generate_population(POPULATION_SIZE)
    for i in range(MAX_GENERATIONS):
        # Seleciona os pais para o cruzamento
        parent1, parent2 = select_parents(population)

        # Realiza o cruzamento
        child = crossover(parent1, parent2)

        # Realiza a mutação
        child = mutate(child, mutation_rate=0.1)

        # Avalia a aptidão do filho
        child_fitness = fitness(child)

        # Se a aptidão do filho for perfeita, retorna o filho
        if child_fitness == 1:
            return child

        # Substitui o indivíduo menos apto da população pelo filho
        population = sorted(population, key=fitness)
        population[0] = child

    # Se não encontrar um indivíduo perfeito, retorna o melhor indivíduo encontrado
    population = sorted(population, key=fitness, reverse=True)
    return population[0]

best_expression = genetic_algorithm()
print("Melhor expressão encontrada: ", best_expression)
print("Valor da expressão: ", evaluate(best_expression))