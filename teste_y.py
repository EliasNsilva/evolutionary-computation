# generate an arithmetic expression
# that produces a given real number
#              example
# input: 5           output: 10 / 2
import random
import operator
import math

# Define a classe de nós da árvore sintática
class Node:
    def __init__(self, left, right, op=None, value=None):
        self.left = left
        self.right = right
        self.op = op
        self.value = value

    def evaluate(self):
        print(self.op)
        if self.op:
            return self.op(self.left.evaluate(), self.right.evaluate())
        else:
            print(self.value)
            return self.value

    def print_tree(self, indent=''):
        if self.op:
            print(f'{indent}({self.op.__name__}')
            self.left.print_tree(indent + '    ')
            self.right.print_tree(indent + '    ')
            print(f'{indent})')
        else:
            print(f'{indent}{self.value}')

def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b else 1

def create_random_tree(depth):
    if depth > 0:
        op = random.choice([add, sub, mul, div])
        left = create_random_tree(depth - 1)
        right = create_random_tree(depth - 1)
        return Node(left, right, op)
    else:
        return Node(None, None, None, random.uniform(-10, 10))

def get_subtrees(node):
    subtrees = []
    if node.left:
        subtrees.append(node.left)
        subtrees.extend(get_subtrees(node.left))
    if node.right:
        subtrees.append(node.right)
        subtrees.extend(get_subtrees(node.right))
    return subtrees

def fitness(node, target):
    return abs(node.evaluate() - target)

def crossover(a, b):
    a_subtree = random.choice(get_subtrees(a))
    b_subtree = random.choice(get_subtrees(b))
    a_subtree.op, b_subtree.op = b_subtree.op, a_subtree.op

def mutation(node):
    sub = random.choice(get_subtrees(node))
    if sub.op:
        sub.op = random.choice([add, sub, mul, div])
    else:
        sub.value = random.uniform(-10, 10)

def roulette_wheel_selection(fitnesses):
    total_fitness = sum(fitnesses)
    r = random.uniform(0, total_fitness)
    i = 0
    while r > 0:
        r -= fitnesses[i]
        i += 1

    return i - 1

def genetic_program(target, pop_size, max_depth, mutation_rate, crossover_rate, max_generations):
    population = [create_random_tree(random.randint(1, max_depth)) for i in range(pop_size)]
    best_fitness = math.inf
    best_individual = None

    for generation in range(max_generations):
        fitnesses = [fitness(node, target) for node in population]
        best_index, best_fitness = min(enumerate(fitnesses), key=operator.itemgetter(1))
        best_individual = population[best_index]

        if best_fitness == 0 or generation == max_generations - 1:
            break

        # parent1 = population[roulette_wheel_selection(fitnesses)]
        # parent2 = population[roulette_wheel_selection(fitnesses)]

        # if random.random() < crossover_rate:
        #     crossover(parent1, parent2)

        # for node in population:
        #     if random.random() < mutation_rate:
        #         mutation(node)

        new_population = []
        while len(new_population) < pop_size:
            parent1 = population[roulette_wheel_selection(fitnesses)]
            parent2 = population[roulette_wheel_selection(fitnesses)]
            child = create_random_tree(random.randint(1, max_depth))
            if random.random() < crossover_rate:
                crossover(parent1, parent2)
            if random.random() < mutation_rate:
                mutation(child)
            new_population.append(child)

        population = new_population

    return best_individual

if __name__ == '__main__':
    result = genetic_program(
        target=42,
        pop_size=100,
        max_depth=5,
        mutation_rate=0.1,
        crossover_rate=0.8,
        max_generations=1000)
    print(result.print_tree())