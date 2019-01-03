"""genalg_update_population.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements tests for updating the population

"""
import numpy as np
import timeit
import multiprocessing
import sys
sys.path.append('.')

from gastop import GenAlg, Truss, Evaluator, FitnessFunction, Crossover, Mutator, Selector, utilities

# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init.txt'
config = utilities.init_file_parser(init_file_path)

pop_size = int(1e2)
num_gens = int(1e1)

# Create GenAlg object and assign random fitness scores
ga = GenAlg(config)
ga.initialize_population(pop_size)
for truss in ga.population:
    truss.fitness_score = np.random.random()

setup ='''
import numpy as np
import multiprocessing
from gastop import GenAlg, Truss, Evaluator, FitnessFunction, Crossover, Mutator, Selector, utilities
from __main__ import method1, method2

init_file_path = 'gastop-config/struct_making_test_init.txt'
config = utilities.init_file_parser(init_file_path)

pop_size = int(1e2)
num_gens = int(1e1)

ga = GenAlg(config)
ga.initialize_population(pop_size)
for truss in ga.population:
    truss.fitness_score = np.random.random()
'''

def method1(ga): # Method 1 performs serial loops for crossover/mutation
    # Store parameters for readability
    population = ga.population
    pop_size = ga.ga_params['pop_size']
    percent_crossover = ga.ga_params['percent_crossover']
    percent_mutation = ga.ga_params['percent_mutation']
    num_elite = ga.ga_params['num_elite']

    # Sort population by fitness score (lowest score = most fit)
    population.sort(key=lambda x: x.fitness_score)

    # Calculate parents needed for crossover, ensure even number
    num_crossover = round((pop_size-num_elite)*percent_crossover)
    if (num_crossover % 2) != 0:  # If odd, increment by 1
        num_crossover += 1
    # Calculate parents needed for mutation
    num_mutation = round((pop_size-num_elite)*percent_mutation)
    # Calculate remaining number of trusses in next population
    num_random = pop_size - num_elite - num_crossover - num_mutation
    if num_random < 0:  # Raise exception if input params are unreasonable
        raise RuntimeError('Invalid GenAlg parameters.')

    # Instantiate objects
    selector = Selector(ga.selector_params)
    crossover = Crossover(ga.crossover_params)
    mutator = Mutator(ga.mutator_params)

    # Select parents as indices in current population
    crossover_parents = selector(num_crossover, population)
    mutation_parents = selector(num_mutation, population)

    # Save most fit trusses as elites
    pop_elite = population[:num_elite]

    # Portion of new population formed by crossover
    pop_crossover = []
    for i in range(0, num_crossover, 2):
        parentindex1 = crossover_parents[i]
        parentindex2 = crossover_parents[i+1]
        parent1 = population[parentindex1]
        parent2 = population[parentindex2]
        child1, child2 = crossover(parent1, parent2)
        pop_crossover.extend((child1, child2))

    # Portion of new population formed by mutation
    pop_mutation = []
    for i in range(num_mutation):
        parentindex = mutation_parents[i]
        parent = population[parentindex]
        child = mutator(parent)
        pop_mutation.append(child)

    # Create new random trusses with remaining spots in generation
    pop_random = [ga.generate_random(2) for i in range(num_random)]

    # Append separate lists to form new generation
    population = pop_elite + pop_crossover + pop_mutation + pop_random

    # Update population attribute
    return population

def method2(ga): # Using multithreading
    num_threads = 5
    # Store parameters for readability
    population = ga.population
    pop_size = ga.ga_params['pop_size']
    percent_crossover = ga.ga_params['percent_crossover']
    percent_mutation = ga.ga_params['percent_mutation']
    num_elite = ga.ga_params['num_elite']

    # Sort population by fitness score (lowest score = most fit)
    population.sort(key=lambda x: x.fitness_score)

    # Calculate parents needed for crossover, ensure even number
    num_crossover = round((pop_size-num_elite)*percent_crossover)
    if (num_crossover % 2) != 0:  # If odd, increment by 1
        num_crossover += 1
    # Calculate parents needed for mutation
    num_mutation = round((pop_size-num_elite)*percent_mutation)
    # Calculate remaining number of trusses in next population
    num_random = pop_size - num_elite - num_crossover - num_mutation
    if num_random < 0:  # Raise exception if input params are unreasonable
        raise RuntimeError('Invalid GenAlg parameters.')

    # Instantiate objects
    selector = Selector(ga.selector_params)
    crossover = Crossover(ga.crossover_params)
    mutator = Mutator(ga.mutator_params)

    # Select parents as indices in current population
    crossover_parents = selector(num_crossover, population)
    mutation_parents = selector(num_mutation, population)

    # Save most fit trusses as elites
    pop_elite = population[:num_elite]

    # Portion of new population formed by crossover
    def iter_crossover(i):
        parentindex1 = crossover_parents[i]
        parentindex2 = crossover_parents[i+1]
        parent1 = population[parentindex1]
        parent2 = population[parentindex2]
        child1, child2 = crossover(parent1, parent2)
        return child1, child2

    with multiprocessing.pool.ThreadPool(num_threads) as pool:
        pop_crossover = pool.map(iter_crossover,range(0, num_crossover, 2))
    pop_crossover = [item for sublist in pop_crossover for item in sublist]
    # for i in range(0, num_crossover, 2):
    #     parentindex1 = crossover_parents[i]
    #     parentindex2 = crossover_parents[i+1]
    #     parent1 = population[parentindex1]
    #     parent2 = population[parentindex2]
    #     child1, child2 = crossover(parent1, parent2)
    #     pop_crossover.extend((child1, child2))

    # Portion of new population formed by mutation
    def iter_mutation(i):
        parentindex = mutation_parents[i]
        parent = population[parentindex]
        child = mutator(parent)
        return child

    with multiprocessing.pool.ThreadPool(num_threads) as pool:
        pop_mutation = pool.map(iter_mutation,range(num_mutation))

    # for i in range(num_mutation):
    #     parentindex = mutation_parents[i]
    #     parent = population[parentindex]
    #     child = mutator(parent)
    #     pop_mutation.append(child)

    # Create new random trusses with remaining spots in generation
    pop_random = [ga.generate_random(2) for i in range(num_random)]

    # Append separate lists to form new generation
    population = pop_elite + pop_crossover + pop_mutation + pop_random

    # Update population attribute
    return population

pop1 = method1(ga)
pop2 = method2(ga)
# print(pop1,len(pop1))
# print(pop2,len(pop2))


test1 = '''pop1 = method1(ga)'''
test2 = '''pop2 = method2(ga)'''

ntests = int(1e1)

time1 = timeit.timeit(setup=setup,stmt=test1,number=ntests)
time2 = timeit.timeit(setup=setup,stmt=test2,number=ntests)

print('method1: ' + str(time1))
print('method2: ' + str(time2))
