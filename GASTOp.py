import numpy as np
import matplotlib.pyplot as plt
import GenAlg
import Eval
import FitnessFunction
import utilities

# Parse input paramters from init.txt file
init_file_path = 'struct_making_test_init.txt'
config = utilities.init_file_parser(init_file_path)

ga_params = config['ga_params']
random_params = config['random_params']
crossover_params = config['crossover_params']
mutator_params = config['mutator_params']
selector_params = config['selector_params']
evaluator_params = config['evaluator_params']
fitness_params = config['fitness_params']


pop_size = ga_params['pop_size']
num_gens = ga_params['num_generations']


# Create the Evaluator Object
evaluator = Eval.Eval(**evaluator_params)

# Create a Fitness Function Object
fitness_function = FitnessFunction.FitnessFunction(**fitness_params)

# Create the Genetic Algorithm Object
ga = GenAlg.GenAlg(ga_params, mutator_params, random_params, crossover_params, selector_params,
                   evaluator, fitness_function)
ga.initialize_population(pop_size)
best, progress_history = ga.run(num_gens, 2)


print(best.rand_nodes)
print(best.fitness_score)
utilities.truss_plot(best, random_params['domain'].T)
