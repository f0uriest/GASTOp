#!/usr/bin/env python3

import unittest
import numpy as np
import random

from gastop import Selector, Truss


class TestSelector(unittest.TestCase):  # Cristian
    def testInvSqrRankProp(self):
        # Tests the inverse_square_rank_probability method of Selector()
        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])
        pop_size = int(1e3)
        population = [Truss(nodes, nodes, edges, properties)
                      for i in range(pop_size)]
        for truss in population:
            truss.fitness_score = random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        sel_params = {'method': 'inverse_square_rank_probability',
                      'tourn_size': None,
                      'tourn_prob': None}
        selector = Selector(sel_params)

        num_parents = int(1e6)
        parents = selector(num_parents, population)

        unique, counts = np.unique(parents, return_counts=True)
        # unique_missing = [x for x in range(pop_size) if x not in unique]
        # counts = np.append(counts,np.zeros(len(unique_missing)))
        # counts = np.insert(counts,unique_missing,np.zeros(len(unique_missing)))
        # print(counts.size)
        distribution = counts/num_parents
        # print(distribution)

        true_distribution = 1/np.sqrt(np.array(range(1, pop_size+1)))
        true_sum = np.sum(true_distribution)
        true_distribution = true_distribution/true_sum
        # print(true_distribution)

        error = true_distribution - distribution
        max_err = np.amax(error)
        # print(max_err)

        # print(parents,parents.shape,parents.max())

        self.assertAlmostEqual(max_err/pop_size, 0, places=3)
        self.assertEqual(num_parents, len(parents))

    def testTournament(self):
        # Tests the tournament method of Selector()
        nodes = np.array([[1, 2, 3], [2, 3, 4]])
        edges = np.array([[0, 1]])
        properties = np.array([[0, 3]])

        pop_size = int(1e2)
        population = [Truss(nodes, nodes, edges, properties)
                      for i in range(pop_size)]
        for truss in population:
            truss.fitness_score = random.random()

        population.sort(key=lambda x: x.fitness_score)
        # print([x.fitness_score for x in population])

        sel_params = {'method': 'tournament',
                      'tourn_size': 25,
                      'tourn_prob': 0.5}
        selector = Selector(sel_params)

        num_parents = int(1e2)
        parents = selector(num_parents, population)

        unique, counts = np.unique(parents, return_counts=True)
        distribution = counts/num_parents
        # print(distribution)

        # print(parents,parents.shape,parents.max())

        self.assertEqual(num_parents, len(parents))
        self.assertTrue(parents.max() < pop_size)


if __name__ == "__main__":
    unittest.main()
