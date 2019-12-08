import random
import pygame
import math

pygame.init()

screen = pygame.display.set_mode((500, 500))

class Bot:
    def __init__(self, pos, color, brain):
        self.pos = pos
        self.color = color
        self.brain = brain
        self.orientation = 0

        self.food_eaten = 0

def roulette(bots):
    total_fitness = 0

    for bot in bots:
        total_fitness += bot.food_eaten
    
    random_point = random.randint(0, total_fitness)

    c = 0
    for bot in bots:
        c += bot.food_eaten

        if c > random_point:
            return bot


def crossover(brain1, brain2):
    input_size = len(brain1[0])
    hidden_size = len(brain1[0][0])
    output_size = len(brain1[1][0])

    flat_input_brain1 = [item for sublist in brain1[0] for item in sublist]
    flat_hidden_brain1 = [item for sublist in brain1[1] for item in sublist]

    flat_input_brain2 = [item for sublist in brain2[0] for item in sublist]
    flat_hidden_brain2 = [item for sublist in brain2[1] for item in sublist]

    complete_flat_brain1 = flat_input_brain1 + flat_hidden_brain1
    complete_flat_brain2 = flat_input_brain2 + flat_hidden_brain2

    crossover_point = random.randint(0, len(complete_flat_brain1))

    kid1 = complete_flat_brain1[ :crossover_point] + complete_flat_brain2[crossover_point: ]
    kid2 = complete_flat_brain2[ :crossover_point] + complete_flat_brain1[crossover_point: ]

    reconstructed_brain1 = [[], []]
    reconstructed_brain2 = [[], []]

    for row in range (input_size):
        subarray = []
        for column in range (hidden_size):
            subarray.append(kid1[row * hidden_size + column])
        
        reconstructed_brain1[0].append(subarray)
    
    for row in range (hidden_size):
        subarray = []
        for column in range (output_size):
            subarray.append(kid1[input_size * hidden_size + row * output_size + column])
        
        reconstructed_brain1[1].append(subarray)
    
    
    for row in range (input_size):
        subarray = []
        for column in range (hidden_size):
            subarray.append(kid1[row * hidden_size + column])
        
        reconstructed_brain2[0].append(subarray)
    
    for row in range (hidden_size):
        subarray = []
        for column in range (output_size):
            subarray.append(kid1[input_size * hidden_size + row * output_size + column])
        
        reconstructed_brain2[1].append(subarray)
    
    return reconstructed_brain1, reconstructed_brain2

def generate_random_brain(hidden_size, input_size, output_size):
    input_to_hidden_weights = [[random.gauss(0, 1) for i in range (hidden_size)] for j in range (input_size)]
    hidden_to_output_weights = [[random.gauss(0, 1) for i in range (output_size)] for j in range (hidden_size)]
    return input_to_hidden_weights, hidden_to_output_weights

def forward(brain, inputs):
    hidden_values = [0 for h in range(len(brain[0][0]))]
    for i in range(len(brain[0])):
        for h in range(len(brain[0][0])):
            hidden_values[h] += inputs[i] * brain[0][i][h]
    
    for i in range(len(hidden_values)):
        hidden_values[i] = sigmoid_func(hidden_values[i])

    #This next part is from hidden to output

    output_values = [0 for h in range(len(brain[1][0]))]
    for h in range(len(brain[1])):
        for o in range(len(brain[1][0])):
            output_values[o] += hidden_values[h] * brain[1][h][o]
    
    for i in range(len(output_values)):
        output_values[i] = sigmoid_func(output_values[i])

    return output_values


def sigmoid_func(number):
        result = 1 / (1 + 2.718 ** -number)
        return result

bots = []

for i in range(40):
    brain = generate_random_brain(10, 2, 1)

    bots.append(Bot([random.randint(0, 500), random.randint(0, 500)], (0, 0, 0), brain))

done = False

food = [[random.randint(0, 500), random.randint(0, 500)] for i in range (20)]

while done != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    for bot in bots:
        smallest = 99999999999999
        food_index = 0

        for i, item in enumerate(food):
            distance = math.sqrt((bot.pos[0] - item[0]) ** 2 + (bot.pos[1] - item[1]) ** 2)

            if distance < smallest:
                smallest = distance
                food_index = i           
   
        vx = food[food_index][0] - bot.pos[0] 
        vy = food[food_index][1] - bot.pos[1]

        if smallest < (7 + 5):
            del food[food_index]
            food.append([random.randint(0, 500), random.randint(0, 500)])
            bot.food_eaten += 1

        mag = math.sqrt(vx ** 2 + vy ** 2)

        vx /= mag
        vy /= mag

        output = forward(bot.brain, [vx, vy])
        net_movement = output[0] * 2 - 0.5

        bot.orientation += net_movement 
        bot.pos[0] += math.cos(math.radians(bot.orientation)) * 0.2
        bot.pos[1] += math.sin(math.radians(bot.orientation)) * 0.2


        pygame.draw.line(screen, (bot.color), (int(bot.pos[0]), int(bot.pos[1])), (int(bot.pos[0]) + math.cos(math.radians(bot.orientation)) * 10, int(bot.pos[1]) + math.sin(math.radians(bot.orientation)) * 10), 2)
        pygame.draw.circle(screen, (bot.color), (int(bot.pos[0]), int(bot.pos[1])), 7 + bot.food_eaten, 1)

    for item in food:
        pygame.draw.circle(screen, (0, 255, 0), item, 5)

    pygame.display.flip()
