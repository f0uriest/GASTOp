#!/usr/bin/env python3

import unittest
import numpy as np
import numpy.testing as npt

import GenAlg
import Truss

class TestGenerateRandom(unittest.TestCase):
    def test_(self):

        ga = GenAlg(ga_params,mutate_params,crossover_params,selector_params,
             evaluator, fitness_function)

        ga.initialize_population(pop_size)

        for i in range(ga.pop_size):
            for
            self.assertTrue()






class TestGenAlg(unittest.TestCase):

    def testTruss(self):

        nodes = np.array([[1,2,3],[2,3,4]])
        edges = np.array([[0,1]])
        properties = np.array([[0,3]])

        pop_size = 10
        population = [Truss.Truss(nodes,edges,properties) for i in range(pop_size)]

        for truss in population:
            truss.fos = random.random()

        population.sort(key=lambda x: x.fos)
                # print([x.fitness_score for x in population])
        #dumb GA run
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        plt.ylabel('fos')
        plt.xlabel('iteration')
        #
        GA = GenAlg()#
        for current_gen in range(num_generations): # Loop over all generations:
