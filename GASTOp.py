import numpy as np
import matplotlib.pyplot as plt
import GenAlg
import Eval
import FitnessFunction
import utilities

# Parse input paramters from init.txt file
init_file_path = 'init.txt'
config = utilities.init_file_parser(init_file_path)

ga_params = config['ga_params']
random_params = config['random_params']
crossover_params = config['crossover_params']
mutate_params = config['mutate_params']
selector_params = config['selector_params']

pop_size = ga_params['pop_size']
num_gens = ga_params['num_generations']

# Stand ins for stuff to be parsed later
properties_df = 0
evaluator = 0

# boundaries = Boundaries.Boundaries(0, 0, 0, 0)  # just for testing

# Create the Evaluator Object
evaluator = Eval.Eval(struct_solver='blank_test',
                      mass_solver='blank_test',
                      interferences_solver='blank_test',
                      boundary_conditions=0,
                      beam_dict=0)

# Create a Fitness Function Object
fitness_function = FitnessFunction.FitnessFunction('rastrigin', 0)

# Create the Genetic Algorithm Object
ga = GenAlg.GenAlg(ga_params, mutate_params, random_params, crossover_params, selector_params,
                   evaluator, fitness_function)
ga.initialize_population(pop_size)
best, progress_history = ga.run(num_gens, 2)


print(best.rand_nodes)
print(best.fitness_score)


# Read in the Possible Materials input file and create objects for each one
"""
Call function to build beam dictionary. Put function in utilities.
"""
#material_dict = create_material_dict(input_file)
