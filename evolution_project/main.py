import random

character_to_binary = {}
binary_to_character = {}

characters = '0123456789+-/*  '
for i in range (len(characters)):
    b = bin(i)[2:]
    b = '0' * (4 - len(b)) + b
    character_to_binary[characters[i]] = b
    binary_to_character[b] = characters[i] 
    

def random_genome():
    genome = ""

    for i in range(100):
        genome += str(random.randint(0, 1))
    
    return genome

def decode_genome(genome):
    expression = ""

    for i in range(0, len(genome), 4):
        genome[i : i + 4]
        chunk = genome[i : i + 4]
        expression += binary_to_character[chunk]
    
    cleaned_expression = " "
    expecting = "number"

    for c in expression:
        if c in "123456789" and expecting == "number":
            if c != '0' and cleaned_expression[-1] not in '0123456789':
                cleaned_expression += c 
        elif c in "+-/*" and cleaned_expression[-1] not in "+-/*":
            cleaned_expression += c

    if cleaned_expression[1] in "+-/*":
        cleaned_expression = cleaned_expression[2:]
    if cleaned_expression[-1] in "+-*/":
        cleaned_expression = cleaned_expression[:-1]
    
    return cleaned_expression
    
def fitness(num):
    f = -1 * ((1333 - num) ** 2)
    return f

def reproduction(parent1, parent2):
    crossover = random.randint(0, len(parent1) - 1)
    offspring = parent1[:crossover] + parent2[crossover:]
    return offspring

def mutation(genome):
    mutated_genome = ""

    for g in genome:
        random_num = random.randint(0, 100)
        if random_num == 1:
            mutated_genome += ['1', '0'][int(g)]

        else:
            mutated_genome += g
    
    return mutated_genome

def roulette(genomes, total_fitness):

    
    bar = sum(total_fitness)
    random_point = random.randint(0, int(bar))
    counter = 0

    for i, c in enumerate(total_fitness):
        counter += c
        if counter >= random_point:
            return genomes[i]

population = [random_genome() for i in range (100)]

done = False
c = 0
while not done:
    c += 1
    print(c)

    new_gen = [] 

    total_fitness = []
    for g in population:
        decoded_genome = decode_genome(g)
        evaluated_genome = eval(decoded_genome)
        genome_fitness = fitness(evaluated_genome)
        total_fitness.append(genome_fitness)
    
    smallest_fitness = min(total_fitness)

    for g in range(len(total_fitness)):
        total_fitness[g] += -smallest_fitness

    for i in range (100):
        parent1 = roulette(population, total_fitness)
        parent2 = roulette(population, total_fitness)

        offspring = mutation(reproduction(parent1, parent2))
        new_gen.append(offspring)

    population = new_gen

    for g in population:
        decoded = decode_genome(g)
        if (abs(eval(decoded) - 1333) < 0.01):
            print(decoded)
            done = True


#print(character_to_binary)
#print(binary_to_character)


