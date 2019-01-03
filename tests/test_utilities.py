"""test_utilities.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the Utilities class

"""
#!/usr/bin/env python3

import unittest
import numpy as np
from gastop import Truss, utilities


class TestUtilities_Cristian(unittest.TestCase):  # Cristian
    def testInitFileParser(self):
        init_file_path = 'gastop-config/boolean_parse_test_init.txt'
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
        self.assertTrue(config['general']['bool0'] is False)
        self.assertTrue(config['general']['bool1'] is True)
        self.assertTrue(config['general']['boolnone'] is None)


class TestTrussPlot(unittest.TestCase):
    def test_truss_plot(self):
        user_spec_nodes = np.array([[-1, -1, 0], [-1, 1, 0]])
        rand_nodes = np.array([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
        edges = np.array([[0, 1], [1, 2], [2, 3], [3, 0],
                          [0, 4], [1, 4], [2, 4], [3, 4]])
        properties = np.zeros(8)
        loads = np.concatenate((np.zeros((4, 6)), np.array(
            [[-100, 0, -100, 0, 0, 0]])), axis=0).reshape(5, 6, 1)
        fixtures = np.concatenate(
            (np.ones((4, 6)), np.zeros((1, 6))), axis=0).reshape(5, 6, 1)
        load_scale = .005
        def_scale = 10
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        truss.deflection = np.concatenate((np.zeros((4, 6)), np.array(
            [[-.01, 0, -.01, 0, 0, 0]])), axis=0).reshape(5, 6, 1)
        domain = np.array([[-1.5, 1.5], [-1.5, 1.5], [0, 1.5]])
        truss.plot(domain, loads, fixtures, True, load_scale, def_scale)


if __name__ == "__main__":
    unittest.main()
