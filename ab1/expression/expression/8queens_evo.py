import random
def view(li, index):
    print()
    print(f"Solution number {index + 1}: ", end='') #Número de soluções
    print(li)
    print()

    for i in range(8): #Criando tabuleiro
        x = li[i] - 1
        for j in range(8):
            if j == x:
                print('[R]', end='')
            else:
                print('[ ]', end='')
        print()
    print()

def heuristica(instance):
    heuristica = []
    for i in range(len(instance)):
        j = i - 1
        heuristica.append(0)
        while j >= 0:
            if instance[i] == instance[j] or (abs(instance[i] - instance[j]) == abs(i - j)):
                heuristica[i] += 1
            j -= 1
        j = i + 1
        while j < len(instance):
            if instance[i] == instance[j] or (abs(instance[i] - instance[j]) == abs(i - j)):
                heuristica[i] += 1
            j += 1
    return heuristica

def getFitness(instance): #Criando fitness
    clashes = 0
    for i in range(len(instance) - 1):
        for j in range(i + 1, len(instance)):
            if instance[i] == instance[j]:
                clashes += 1
    for i in range(len(instance) - 1):
        for j in range(i + 1, len(instance)):
            if abs(instance[j] - instance[i]) == abs(j - i):
                clashes += 1
    return 28 - clashes

def build_child(instance1, instance2, crossOver):
    newInstance = []
    for i in range(crossOver):
        newInstance.append(instance1[random.randint(0, 7)])
    for i in range(crossOver, 8):
        newInstance.append(instance2[random.randint(0, 7)])
    return newInstance

def changeChilds(co):
    global father, mother, child1, child2, crossover #Possibilidades
    crossover = co
    child1 = build_child(father, mother, crossover)
    child2 = build_child(mother, father, crossover)

def changeChromosome(li):
    global crossover, father, mother
    newchange = -1
    while newchange != 0:
        newchange = 0
        tmpli = li
        getHur = heuristica(tmpli)
        index = getHur.index(max(getHur))
        maxFitness = getFitness(tmpli)
        for i in range(1, 9):
            tmpli[index] = i
            if getFitness(tmpli) > maxFitness:
                maxFitness = getFitness(tmpli)
                newchange = i
            tmpli = li
        if newchange == 0:
            for i in range(len(li) - 1):
                for j in range(i + 1, len(li)):
                    if li[i] == li[j]:
                        li[j] = random.randint(1, 8)
        else:
            li[index] = newchange

if __name__ == "__main__":
    print("Select the number of queens: ")
    numberOfSolutions = int(input())
    solutions = []
    crossover = 4
    while len(solutions) < numberOfSolutions:
        father = []
        mother = []
        for i in range(8):
            father.append(random.randint(1, 8))
            mother.append(random.randint(1, 8))
        fitnessFather = getFitness(father)
        fitnessMother = getFitness(mother)
        while fitnessFather != 28 and fitnessMother != 28:
            changeChilds(crossover)
            changeChromosome(child1)
            changeChromosome(child2)
            fitnessFather = getFitness(child1)
            fitnessMother = getFitness(child2)
            father = child1
            mother = child2
            print(father)
            print(mother)
        if getFitness(father) == 28:
            if father not in solutions:
                solutions.append(father)
        else:
            if mother not in solutions:
                solutions.append(mother)

    print("####################### Solutions #####################")
    print(f"The number of solutions you wanted: {numberOfSolutions}")

    for i in range(len(solutions)):
        view(solutions[i], i)
    print("#######################################################")