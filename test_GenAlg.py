#!/usr/bin/env python3

import unittest
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt
from matplotlib import style
import GenAlg
import Truss


class TestGenAlg_Dan(unittest.TestCase):
    def test_(self):

        ga = GenAlg(ga_params,mutate_params,crossover_params,selector_params,
             evaluator, fitness_function)

        ga.initialize_population(pop_size)

        for i in range(ga.pop_size):

            self.assertTrue()






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

        GA = GenAlg.GenAlg(0,0,0,0,0,0,0)#put zeros in here

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
