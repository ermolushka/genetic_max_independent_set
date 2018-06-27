import networkx as nx
from numpy.random import random_integers
import numpy as np

G=nx.Graph()
G.add_nodes_from([x for x in range(1,8)])
G.add_edges_from([(1,2),(2,3), (3,4), (4,6), (5,6), (5,7), (6,7)])

population_size = 50


n = 7 # edges
epochs = 700

right_answer = [1,0,1,0,1,1,0,1,0,1]


def create_population():

    population = []
    for j in range(population_size):
        candidate = []
        for x in range(n):
            candidate.append(random_integers(0,1))
        population.append(candidate)

    return population

def fitness_function_all(population): # for the whole population

    miss_rate = 0
    for item in population:
        
        miss_rate += fitness_function(item)
        
    return miss_rate


def fitness_function(item):

    ajacency = np.array(nx.adjacency_matrix(G).todense()).tolist()
    remove_indices = []
    for x in range(len(item)):
        if item[x] == 0:
            remove_indices.append(x)
    for index in sorted(remove_indices, reverse=True):
        del ajacency[index]

    for x in ajacency:
        for index in sorted(remove_indices, reverse=True):
            del x[index]

    flattened = [y for x in ajacency for y in x]
    return sum(item) - sum(flattened)


def best_from_population(population):

    MIN = fitness_function(population[0])
    best = []
    for item in population[1:]:
        if fitness_function(item) > MIN:
            MIN = fitness_function(item)
            best = item
    return MIN, best

def selection(population): # select parents
    # random pair from the best n parents
    losses = {}
    for j in range(len(population)):
        losses[j] = fitness_function(population[j])
    result = {}
    for key in sorted(losses, key=losses.get, reverse=True)[:5]:
        result.update({key: losses[key]})
    all_parents = list(result.keys())
    first, second = random_integers(0,4), random_integers(0,3)
    parents = []
    parents.append(all_parents[first])
    all_parents.remove(all_parents[first])
    parents.append(all_parents[second])
    return parents

def two_point_crossingover(parents, population):

    first, second = random_integers(0,3), random_integers(4,6)
    first_change = population[parents[1]][first+1:second+1]
    second_change = population[parents[0]][first+1:second+1]

    parent1 = population[parents[0]][:first+1] + first_change + population[parents[0]][second+1:]
    parent2 = population[parents[1]][:first+1] + second_change + population[parents[1]][second+1:]
    final_parents = [parent1, parent2]

    return final_parents[random_integers(0,1)]

def inversion(item):
    inversion_point = random_integers(0,6)
    last_point = 9
    item[inversion_point:last_point+1] = reversed(item[inversion_point:last_point+1])
    return item

def mutate(item):
    mutate_point = random_integers(0,4)
    #print(item)
    item[mutate_point], item[mutate_point+1] = item[mutate_point+1], item[mutate_point]
    return item

def main():

    population = create_population()
    step = 0
    max_fitness, best = best_from_population(population)
    for j in range(epochs):
        parents = selection(population)
        aim = two_point_crossingover(parents, population)
        inverted = inversion(aim)
        mutated = mutate(inverted)
        to_drop = random_integers(0,population_size-1)
        population[to_drop] = mutated
        print("epoch: ", str(j))
        print("best: ", best_from_population(population)[0])
        if best_from_population(population)[0] > max_fitness:
            max_fitness, best = best_from_population(population)
        step += 1
    print("best final: ", max_fitness)
    print("best choice: ", best)

main()




