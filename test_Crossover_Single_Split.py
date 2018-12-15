#!/usr/bin/env python3

import unittest
import numpy as np

import Crossover

'''
array1 = np.arange(1,11,1).reshape((10,1))
array2 = np.arange(11,21,1).reshape((10,1))
myCrossover = Crossover.Crossover([])
child_1, child_2 = myCrossover.single_point_split(array1,array2)
print('child_1 =\n',child_1)
print('child_2 =\n',child_2)
'''


class TestCrossover_singlepointsplit(unittest.TestCase):
    def test_Basic(self):
        # Change point to 5 before running this test
        array1 = np.arange(1, 11, 1).reshape((10, 1))
        array2 = np.arange(11, 21, 1).reshape((10, 1))
        myCrossover = Crossover.Crossover([])
        children = myCrossover.single_point_split(array1, array2)

        np.testing.assert_array_equal(
            children[0].T, [(1, 2, 3, 4, 5, 16, 17, 18, 19, 20)])
        np.testing.assert_array_equal(
            children[1].T, [(11, 12, 13, 14, 15, 6, 7, 8, 9, 10)])


if __name__ == '__main__':
    unittest.main()
