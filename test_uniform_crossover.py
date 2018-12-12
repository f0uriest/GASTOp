#!/usr/bin/env python3

import unittest
import numpy as np

import Crossover

class TestCrossoverPaul(unittest.TestCase):
    def testZeros(self):
        truss_1 = np.zeros(10, dtype=int)
        truss_2 = np.zeros(10, dtype=int)

        my_uniform_crossover = Crossover.Crossover([])
        result = my_uniform_crossover.uniform_crossover(truss_1, truss_2)

        self.assert_array_equal(result[0], truss_1)
        self.assert_array_equal(result[1], truss_2)

        
if __name__ == "__main__":
    unittest.main()
