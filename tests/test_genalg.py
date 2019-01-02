#!/usr/bin/env python3

import unittest
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt
from matplotlib import style
import json
import sys
from tqdm import tqdm, tqdm_notebook, tnrange
import time
# sys.path.append('../')
# sys.path.append('.')
# print(sys.path)


#from gastop import GenAlg, Truss, Evaluator, FitnessFunction, utilities

from gastop import GenAlg, Truss, Evaluator, FitnessFunction, utilities, ProgMon


# Parse input paramters from init.txt file
init_file_path = 'gastop-config/struct_making_test_init.txt'
config = utilities.init_file_parser(init_file_path)


# properties_df = 0

pop_size = int(1e4)
num_gens = int(1e2)

# boundaries = Boundaries(#Input here);

# Create the Evaluator Object
#evaluator = Eval(blah)

# Create a Fitness Function Object


class TestGenAlg_Cristian(unittest.TestCase):  # Cristian
    def testUpdatePopulation(self):
        # Create GenAlg object and assign random fitness scores
        pop_size = int(1e4)
        ga = GenAlg(init_file_path)
        ga.initialize_population(pop_size)
        for truss in ga.population:
            truss.fitness_score = np.random.random()

        ga.update_population()

        # Check that population is sorted by fitness_score
        fitness = [
            truss.fitness_score for truss in ga.population][:config['ga_params']['num_elite']]
        self.assertTrue(sorted(fitness) == fitness)

        for truss in ga.population:
            self.assertTrue(type(truss) is Truss)
            self.assertTrue(type(truss.user_spec_nodes) is np.ndarray)
            self.assertTrue(type(truss.rand_nodes) is np.ndarray)
            self.assertTrue(type(truss.edges) is np.ndarray)
            self.assertTrue(type(truss.properties) is np.ndarray)

    def testSaveLoadState(self):
        # Parse input parameters from init file
        init_file_path = 'gastop-config/struct_making_test_init.txt'
        config = utilities.init_file_parser(init_file_path)

        # Create GenAlg object
        pop_size = int(1e4)
        ga = GenAlg(config)
        ga.initialize_population(pop_size)

        # Save and reload
        ga.save_state()
        config, population = ga.load_state()

        # Test config
        self.assertTrue(type(config['ga_params']['num_elite']) is int)
        self.assertTrue(
            type(config['ga_params']['percent_crossover']) is float)
        self.assertTrue(type(config['mutator_params']['node_mutator_params']['boundaries'])
                        is type(np.array([1, 1])))
        self.assertTrue(type(config['mutator_params']['node_mutator_params']['int_flag'])
                        is bool)

        # Test population
        for truss in population:
            self.assertTrue(type(truss) is Truss)
            self.assertTrue(type(truss.user_spec_nodes) is np.ndarray)
            self.assertTrue(type(truss.rand_nodes) is np.ndarray)
            self.assertTrue(type(truss.edges) is np.ndarray)
            self.assertTrue(type(truss.properties) is np.ndarray)
        # print(config)
        # print([truss for truss in population])


class TestGenAlg_Dan(unittest.TestCase):
    def test_nodes_in_domain(self):

        # Create the Genetic Algorithm Object
        ga = GenAlg(config)
        ga.initialize_population(pop_size)

        for truss in ga.population:
            for node in truss.rand_nodes:
                self.assertTrue(node[0] > ga.random_params['domain'][0, 0])
                self.assertTrue(node[0] < ga.random_params['domain'][1, 0])
                self.assertTrue(node[1] > ga.random_params['domain'][0, 1])
                self.assertTrue(node[1] < ga.random_params['domain'][1, 1])
                self.assertTrue(node[2] > ga.random_params['domain'][0, 2])
                self.assertTrue(node[2] < ga.random_params['domain'][1, 2])


class TestGenAlg_SFR(unittest.TestCase):

    def testProgressPlotClass(self):
        user_spec_nodes = np.array([[]]).reshape(0, 3)
        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])

        pop_size = 10
        population = [Truss(
            user_spec_nodes, nodes, edges, properties) for i in range(pop_size)]

        for truss in population:
            truss.fitness_score = np.random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        GA = GenAlg(config)

        GA.population = population
        progress_display = 2
        num_generations = 20

        progress = ProgMon(progress_display,num_generations)

        #

        # Loop over all generations:
        for current_gen in range(num_generations):
            progress.progress_monitor(current_gen,population)
            for truss in GA.population:
                #truss.fos = np.random.random()
                truss.fitness_score = truss.fitness_score + 5.0
        plt.show()  # sfr, keep plot from closing right after this completes, terminal will hang until this is closed
        return GA.population[0], GA.pop_progress

    def testProgressBar2(self):
        # this doesnt quite work yet, showing all progress bars at the end instead of iteratively
        user_spec_nodes = np.array([[]]).reshape(0, 3)

        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])

        pop_size = 10
        population = [Truss(user_spec_nodes, nodes, edges, properties)
                      for i in range(pop_size)]

        for truss in population:
            truss.fitness_score = np.random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        GA = GenAlg(config)

        GA.population = population
        progress_display = 1

        ax1 = []
        num_generations = 20
        progress = ProgMon(progress_display,num_generations)

        #t = tqdm(total=num_generations,leave=False)
        # Loop over all generations:
        for current_gen in tqdm_notebook(range(num_generations),desc='Generation'):
            progress.progress_monitor(current_gen,population)
            # t.update(current_gen)
            time.sleep(0.05)
            for truss in tqdm_notebook(GA.population,desc='truss'):
                #truss.fos = np.random.random()
                truss.fitness_score = truss.fitness_score + 5.0
        # t.close()
        return GA.population[0], GA.pop_progress


    def testProgressBar(self):
        # this doesnt quite work yet, showing all progress bars at the end instead of iteratively
        user_spec_nodes = np.array([[]]).reshape(0, 3)

        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])

        pop_size = 10
        population = [Truss(user_spec_nodes, nodes, edges, properties)
                      for i in range(pop_size)]

        for truss in population:
            truss.fitness_score = np.random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        GA = GenAlg(config)

        GA.population = population
        progress_display = 1
        # dumb GA run
        ax1 = []
        num_generations = 20
        progress = ProgMon(progress_display,num_generations)
        #t = tqdm(total=num_generations,leave=False)
        # Loop over all generations:
        for current_gen in tqdm(range(num_generations)):
            progress.progress_monitor(current_gen,population)
            # t.update(current_gen)
            time.sleep(0.05)
            for truss in GA.population:
                #truss.fos = np.random.random()
                truss.fitness_score = truss.fitness_score + 5.0
        # t.close()
        return GA.population[0], GA.pop_progress

    # def testProgressPlot(self):
    #     user_spec_nodes = np.array([[]]).reshape(0, 3)
    #     nodes = np.array([[1, 2, 3], [2, 3, 4]])
    #     edges = np.array([[0, 1]])
    #     properties = np.array([[0, 3]])
    #
    #     pop_size = 10
    #     population = [Truss(
    #         user_spec_nodes, nodes, edges, properties) for i in range(pop_size)]
    #
    #     for truss in population:
    #         truss.fitness_score = np.random.random()
    #
    #     population.sort(key=lambda x: x.fitness_score)
    #     # print([x.fitness_score for x in population])
    #
    #     GA = GenAlg(config)
    #
    #     GA.population = population
    #     progress_display = 2
    #     num_generations = 20
    #     # dumb GA run
    #     fig = plt.figure()
    #     ax1 = fig.add_subplot(1, 1, 1)
    #     plt.ylabel('fitscore')
    #     plt.xlabel('iteration')
    #     plt.xlim(0,num_generations)
    #
    #     #
    #
    #     # Loop over all generations:
    #     for current_gen in range(num_generations):
    #         GA.progress_monitor(current_gen, progress_display, ax1)
    #         for truss in GA.population:
    #             #truss.fos = np.random.random()
    #             truss.fitness_score = truss.fitness_score + 5.0
    #     plt.show()  # sfr, keep plot from closing right after this completes, terminal will hang until this is closed
    #     return GA.population[0], GA.pop_progress
    #
    #     #GA = GenAlg()
    #     #pop_test = GA.initialize_population(10)
    #
    #     # fos = [i.fos for i in population] #extracts fos for each truss object in population
    #
    #     # note to susan: look up map() and filter()


class TestGenAlgRC(unittest.TestCase):

    def testInvalidCrossover(self):
        """Tests genalg when % crossover + % mutation >1"""

        config = utilities.init_file_parser(init_file_path)
        config['ga_params']['percent_crossover'] = .6
        config['ga_params']['percent_mutation'] = .6
        ga = GenAlg(config)
        ga.initialize_population(100)
        for t in ga.population:
            t.fitness_score = np.random.random()
        self.assertRaises(RuntimeError, ga.update_population)

        bad_path = 'gastop-config/error_config.txt'
        self.assertRaises(RuntimeError, utilities.init_file_parser, bad_path)

    def testOddNumCrossover(self):
        """Tests genalg when crossover number is odd"""

        config = utilities.init_file_parser(init_file_path)
        config['ga_params']['percent_crossover'] = 1
        config['ga_params']['percent_mutation'] = 0
        config['ga_params']['num_elite'] = 5
        ga = GenAlg(config)
        ga.initialize_population(100)
        ga.run(num_generations=2)
        self.assertAlmostEqual(len(ga.population), 100)

        # test zero crossover
        config['ga_params']['percent_crossover'] = 0
        config['ga_params']['percent_mutation'] = 1
        ga = GenAlg(config)
        ga.initialize_population(100)
        ga.run(num_generations=2)
        self.assertAlmostEqual(len(ga.population), 100)


if __name__ == "__main__":
    unittest.main()
