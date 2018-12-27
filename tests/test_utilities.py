#!/usr/bin/env python3

import unittest
import numpy as np
from gastop import Truss, utilities


class TestUtilities_Cristian(unittest.TestCase):  # Cristian
    def testInitFileParser(self):
        init_file_path = 'gastop-config/struct_making_test_init.txt'
        config = utilities.init_file_parser(init_file_path)
        # for key in config:
        #     print(key)
        #     print(config[key])
        self.assertTrue(type(config['ga_params']['num_elite']) is int)
        self.assertTrue(
            type(config['ga_params']['percent_crossover']) is float)
        self.assertTrue(type(config['mutator_params']['node_mutator_params']['boundaries'])
                        is type(np.array([1, 1])))
        self.assertTrue(type(config['mutator_params']['node_mutator_params']['int_flag'])
                        is bool)


class TestTrussPlot(unittest.TestCase):
    def test_truss_plot(self):
        user_spec_nodes = np.array([[-1, -1, 0],
                                    [-1, 1, 0]])
        rand_nodes = np.array([[1, 1, 0],
                               [1, -1, 0],
                               [0, 0, 1]])
        edges = np.array([[0, 1],
                          [1, 2],
                          [2, 3],
                          [3, 0],
                          [0, 4],
                          [1, 4],
                          [2, 4],
                          [3, 4]])
        properties = np.zeros(8)
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        domain = np.array([[-1.5, 1.5], [-1.5, 1.5], [0, 1.5]])
        utilities.truss_plot(truss, domain)


if __name__ == "__main__":
    unittest.main()
