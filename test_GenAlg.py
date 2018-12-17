#!/usr/bin/env python3

import unittest
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt
from matplotlib import style
import GenAlg
import Truss
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
    'node_crossover_params' : {},
    'edge_crossover_params': {},
    'property_crossover_params': {},
    }

mutate_params = {
    'node_mutator_method': 'gaussian',
    'edge_mutator_method': 'pseudo_bit_flip',
    'property_mutator_method': 'gaussian',

    'node_mutator_params' : {'boundaries': np.array([[-5,5],[-5,5],[-5,5]]),'std':0.2},
    'edge_mutator_params' : {'bounds': np.array([[-1,-1],[10,10]])},
    'property_mutator_params' : {'boundaries': np.array([[-1,10],[-1,10]]), 'std': 2}
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

class TestGenAlg_Dan(unittest.TestCase):
    def test_nodes_in_domain(self):

        # Create the Genetic Algorithm Object
        ga = GenAlg.GenAlg(ga_params,mutate_params,random_params,crossover_params,selector_params,
                     evaluator, fitness_function, properties_df)
        ga.initialize_population(pop_size)

        for truss in ga.population:
            for node in truss.nodes:
                self.assertTrue(node[0] > random_params['domain'][0,0])
                self.assertTrue(node[0] < random_params['domain'][1,0])
                self.assertTrue(node[1] > random_params['domain'][0,1])
                self.assertTrue(node[1] < random_params['domain'][1,1])
                self.assertTrue(node[2] > random_params['domain'][0,2])
                self.assertTrue(node[2] < random_params['domain'][1,2])







class TestGenAlg_SFR(unittest.TestCase):

    def testProgressPlot(self):

        nodes = np.array([[1,2,3],[2,3,4]])
        edges = np.array([[0,1]])
        properties = np.array([[0,3]])

        pop_size = 10
        population = [Truss.Truss(nodes,edges,properties) for i in range(pop_size)]

        for truss in population:
            truss.fos = np.random.random()

        population.sort(key=lambda x: x.fos)
                # print([x.fitness_score for x in population])

        GA = GenAlg.GenAlg(0,0,0,0,0,0,0,0)#put zeros in here

        GA.population = population
        progress_display = 2
        #dumb GA run
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        plt.ylabel('fos')
        plt.xlabel('iteration')
        #
        num_generations = 20
        for current_gen in range(num_generations): # Loop over all generations:
            GA.progress_monitor(current_gen,progress_display,ax1)
            for truss in GA.population:
                #truss.fos = np.random.random()
                truss.fos = truss.fos + 5.0
        plt.show() #sfr, keep plot from closing right after this completes, terminal will hang until this is closed
        return GA.population[0], GA.pop_progress

        #GA = GenAlg()
        #pop_test = GA.initialize_population(10)

        #fos = [i.fos for i in population] #extracts fos for each truss object in population


        #note to susan: look up map() and filter()
if __name__ == "__main__":
    unittest.main()
