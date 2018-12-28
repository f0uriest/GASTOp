import cProfile

import unittest
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt
from matplotlib import style
import json
import sys
sys.path.append('.')

from gastop import GenAlg, Truss, Evaluator, FitnessFunction, utilities

# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init.txt'
config = utilities.init_file_parser(init_file_path)

ga_params = config['ga_params']
random_params = config['random_params']
crossover_params = config['crossover_params']
mutator_params = config['mutator_params']
selector_params = config['selector_params']
evaluator_params = config['evaluator_params']
fitness_params = config['fitness_params']

# properties_df = 0
evaluator = 0

pop_size = int(1e4)
num_gens = int(1e2)

# boundaries = Boundaries(#Input here);

# Create the Evaluator Object
#evaluator = Eval(blah)

# Create a Fitness Function Object
fitness_function = FitnessFunction('rastrigin', 0)
pop_size = int(1e4)
ga = GenAlg(ga_params, mutator_params, random_params, crossover_params, selector_params,
            evaluator, fitness_function)
#ga.initialize_population(pop_size)
cProfile.run('ga.initialize_population(pop_size)')
