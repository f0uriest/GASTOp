#!/usr/bin/env python3

import unittest
import numpy as np

import utilities

class TestUtilities_Cristian(unittest.TestCase): # Cristian
    def testInitFileParser(self):
        init_file_path = 'init.txt'
        config = utilities.init_file_parser(init_file_path)
        # for key in config:
        #     print(key)
        #     print(config[key])
        self.assertTrue(type(config['ga_params']['num_elite']) is int)
        self.assertTrue(type(config['ga_params']['percent_crossover']) is float)
        self.assertTrue(type(config['mutate_params']['node_mutator_params']['boundaries'])\
                        is type(np.array([1,1])))
        self.assertTrue(type(config['mutate_params']['node_mutator_params']['int_flag'])\
                        is bool)


if __name__ == "__main__":
    unittest.main()
