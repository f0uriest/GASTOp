import numpy as np
import matplotlib.pyplot as plt
from gastop import GenAlg, utilities
from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph.output import GraphvizOutput


# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init2.txt'
config = utilities.init_file_parser(init_file_path)

pop_size = config['ga_params']['pop_size']
num_gens = config['ga_params']['num_generations']

conf = Config()
conf.trace_filter = GlobbingFilter(include=['__main__', 'gastop.*'])

graphviz = GraphvizOutput(output_file='filter_exclude4.png')

with PyCallGraph(output=graphviz, config=conf):

    # Create the Genetic Algorithm Object
    ga = GenAlg(config)
    ga.initialize_population(200)
    best, progress_history = ga.run(
        num_generations=10, progress_display=1, num_threads=1)


# con = best.edges.copy()
# matl = best.properties.copy()
# matl = matl[(con[:, 0]) >= 0]
# con = con[(con[:, 0]) >= 0]
# matl = matl[(con[:, 1]) >= 0]
# con = con[(con[:, 1]) >= 0]


# print(best.rand_nodes)
# print(con)
# print(matl)
# print(best.fos)
# print(best.deflection[:, :3, 0])
# best.plot(domain=config['random_params']['domain'].T,
#           loads=config['evaluator_params']['boundary_conditions']['loads'],
#           fixtures=config['evaluator_params']['boundary_conditions']['fixtures'],
#           deflection=True, load_scale=.00001, def_scale=50)
