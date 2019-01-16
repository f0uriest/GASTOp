"""gastop_example_script.py
This file runs the gastop program
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.

"""
from gastop import GenAlg, utilities


# needs to be full path
animation_path = '/Users/susanredmond/Desktop/APC524_FinalProject/animation'
# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init2.txt'

config = utilities.init_file_parser(init_file_path)

pop_size = 1000
num_gens = 50
progress_fitness = True
progress_truss = True

# Create the Genetic Algorithm Object
ga = GenAlg(config)
ga.initialize_population(pop_size)
best, progress_history = ga.run(
    num_generations=num_gens, progress_fitness=progress_fitness,
    progress_truss=progress_truss, num_threads=8)


print(best)

best.plot(domain=config['random_params']['domain'],
          loads=config['evaluator_params']['boundary_conditions']['loads'],
          fixtures=config['evaluator_params']['boundary_conditions']['fixtures'],
          deflection=True, load_scale=.0002, def_scale=50)

#progress_fitness = True
#progress_truss = True
utilities.save_gif(progress_history, progress_fitness, progress_truss,
                   animation_path, num_gens, config, gif_pause=0.5)
