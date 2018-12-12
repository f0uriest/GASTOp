#!/usr/bin/env python3

import unittest
import numpy as np
import random
import math

import Selector
import Truss

class TestSelector(unittest.TestCase): # Cristian
    def testInvSqrRankProp(self):
        # Tests the inverse_square_rank_probability method of Selector()
        nodes = np.array([[1,2,3],[2,3,4]])
        edges = np.array([[0,1]])
        properties = np.array([[0,3]])

        pop_size = 10
        population = [Truss.Truss(nodes,edges,properties) for i in range(pop_size)]
        for truss in population:
            truss.fitness_score = random.random()

        sel_params = {'method': 'inverse_square_rank_probability'}
        selector = Selector.Selector(sel_params)

        num_parents = int(1e4)
        parents = selector(num_parents,population)

        distribution = [parents.count(x)/num_parents for x in range(pop_size)]
        print(distribution)

        # inv_sqr_distribution = [1/math.sqrt(i) for i in range(1,pop_size+1)]
        # sum_inv = sum(inv_sqr_distribution)
        # normalized = [x/sum_inv for x in inv_sqr_distribution]
        # print(normalized,sum(normalized))
        # print(inv_sqr_distribution)
        # self.assertAlmostEqual(distribution,inv_sqr_distribution)
        self.assertEqual(num_parents, len(parents))

if __name__ == "__main__":
    unittest.main()
