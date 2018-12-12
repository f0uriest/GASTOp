import unittest
import numpy as np
import numpy.testing as npt

import GenAlg
import Truss

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
            self.progress_monitor(self.population,current_gen,ax1)
            for current_truss in range(self.pop_size): # Loop over all trusses -> PARALLELIZE. Later
                self.fitness_function(self.population[current_truss]) # Assigns numerical score to each truss
            self.population = self.update_population(self.population) # Determine which members to
        plt.show() #sfr, keep plot from closing right after this completes, terminal will hang until this is closed
        return self.population[0], self.pop_progress

        #GA = GenAlg()
        #pop_test = GA.initialize_population(10)

        fos = [i.fos for i in population] #extracts fos for each truss object in population


        #note to susan: look up map() and filter()
if __name__ == "__main__":
    unittest.main()
