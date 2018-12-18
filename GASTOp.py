import numpy as np
import matplotlib.pyplot as plt
import GenAlg
import Eval
import FitnessFunction
import Boundaries


# Specify set-up things
# for now, declare all variables (will call the function to parse the input file later)
ga_params = {
    # ga_params
    'pop_size' : None,
    'num_elite' : 1, #int, ~10 (the whole truss that get passed)
    'percent_crossover' : 0.4, # double between 0 and 1
    'percent_mutation' : 0.4 # double between 0 and 1
    }

random_params = {
    #Random
    'num_rand_nodes' : 1, # int
    'num_rand_edges' : 10, # int
    'domain' : np.array([[-5,-5,-5],[5,5,5]]), # np array 2x3 [[xmin,ymin,zmin],[xmax,ymax,zmax]]
    'num_material_options' : 10,
    'num_user_spec_nodes' : 0
    }

crossover_params = {
    'node_crossover_method': 'uniform_crossover',
    'edge_crossover_method': 'uniform_crossover',
    'property_crossover_method': 'single_point_split',
    'node_crossover_params' : None,
    'edge_crossover_params': None,
    'property_crossover_params': {},
    }

mutate_params = {
    'node_mutator_method': 'gaussian',
    'edge_mutator_method': 'pseudo_bit_flip',
    'property_mutator_method': 'gaussian',

    'node_mutator_params' : {'boundaries': np.array([[-5,5],[-5,5],[-5,5]]),'std':0.2, 'int_flag':False},
    'edge_mutator_params' : {'bounds': np.array([[-1,-1],[10,10]])},
    'property_mutator_params' : {'boundaries': np.array([[-1,10],[-1,10]]), 'std': 2, 'int_flag':False}
    }

selector_params = {'method': 'inverse_square_rank_probability'}


properties_df = 0
evaluator = 0

pop_size = 10000
num_gens = 100

#boundaries = Boundaries(#Input here);

# Create the Evaluator Object
#evaluator = Eval(blah)

# Create a Fitness Function Object
fitness_function = FitnessFunction.FitnessFunction('rastrigin',0)

# Create the Genetic Algorithm Object
ga = GenAlg.GenAlg(ga_params,mutate_params,random_params,crossover_params,selector_params,
             evaluator, fitness_function, properties_df)
ga.initialize_population(pop_size)
best, progress_history = ga.run(num_gens,2)


print(best.nodes)
print(best.fitness_score)



### Read in the Possible Materials input file and create objects for each one
"""
Call function to build beam dictionary. Put function in utilities.
"""
#material_dict = create_material_dict(input_file)
