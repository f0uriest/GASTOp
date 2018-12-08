import numpy as np
import matplotlib.pyplot as plt
import GenAlg
import Eval
import FitnessFunction
import Boundaries


# Specify set-up things
# for now, declare all variables (will call the function to parse the input file later)

""" INPUT PARAMETERS

    Here are the things needed to initially call GA:
    (num_generations,pop_size,
    num_rand_nodes,num_rand_edges,domain,
    crossover_fraction = 0.5, split_method = None,
    stat_var_nodes,stat_var_edges,stat_var_matlself,
    num_elite,percent_crossover,percent_mutation):
"""
#Susan:
num_generations = 10
pop_size = 100
num_rand_node = 50
snum_rand_edges =
domain = np.array([[0,0],[1,1]])
crossover_fraction = 0.5 # Default - already in function call.
split_method = None # Default - already in function call.
#stat_var_nodes = ,stat_var_edges = ,stat_var_matlself =
#num_elite = ,percent_crossover = ,percent_mutation =
boundaries = Boundaries(#Input here);

# Create the Evaluator Object
#evaluator = Eval(blah)

# Create a Fitness Function Object
fit = FitnessFunction(blah)

# Create the Genetic Algorithm Object
ga = GenAlg(ga_params,mutate_params,crossover_params,selector_params,
             evaluator, fitness_function)
ga.initialize_population(pop_size)
best, progress_history = ga.run(num_gens)






### Read in the Possible Materials input file and create objects for each one
"""
Call function to build beam dictionary. Put function in utilities.
"""
material_dict = create_material_dict(input_file)
