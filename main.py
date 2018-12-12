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

""" Dictionaries to be created:
    # ********
    !self.ga_params = ga_params
    !self.mutate_params = mutate_params
    !self.random_params = random_params
    !self.crossover_params = crossover_params
    self.selector_params = selector_params
    self.population = None
    self.evaluator = evaluator
    self.fitness_function = fitness_function
    # ********
"""
ga_params = {
    # ga_params
    self.pop_size: 100,
    self.num_elite: 10, #int, ~10 (the whole truss that get passed)
    self.percent_crossover: 0.5, # double between 0 and 1
    self.percent_mutation: 0.5 # double between 0 and 1
}

random_params = {
    #Random
    self.num_generations: 10,
    self.num_rand_nodes: 50, # int
    self.num_rand_edges: 50, # int
    self.domain: np.array([[0,0],[1,1]]), # np array 2x3 [[xmin,ymin,zmin],[xmax,ymax,zmax]]
    self.num_material_options: 10
}

crossover_params = {
    # Crossover - different crossovers for edges, nodes, properties
    # *** Will end up in the crossover_params ***
    Edge_crossover_fraction: 0.5, # double between 0 and 1
    #Edge_split_method: 'edge_split_method' # string
    Node_crossover_fraction = node_crossover_fraction
    #Node_split_method = node_split_method
    Materials_crossover_fraction = materials_crossover_fraction
    #Materials_split_method = materials_split_method
}

mutate_params = {
    #Mutation
    self.stat_stdev_nodes: 0.5, # double
    self.stat_stdev_edges: 0.5, # double
    self.stat_stdev_matl: 0.5, # double
    self.pseudo_bit_flip_prob_nodes: 0.5, # double between 0 and 1
    self.pseudo_bit_flip_prob_edges: 0.5, # double between 0 and 1
    self.pseudo_bit_flip_prob_matl: 0.5, # double between 0 and 1
}






#Susan:
#num_generations = 10
#pop_size = 100
#num_rand_node = 50
#snum_rand_edges =
#domain = np.array([[0,0],[1,1]])
#crossover_fraction = 0.5 # Default - already in function call.
#split_method = None # Default - already in function call.
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
