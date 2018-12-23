#!/usr/bin/env python3

import unittest
import numpy as np

import Crossover

class TestCrossover_singlepointsplit(unittest.TestCase): #Amlan

    def test_sanity(self):

        array1 = np.ones((10,1))
        array2 = np.ones((10,1))
        check = np.ones((10,1))

        myCrossover = Crossover.Crossover([])
        children = myCrossover.single_point_split(array1, array2)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

    def test_datatype(self):

        array1 = np.ones((10,1), dtype=np.float64)
        array2 = np.ones((10,1), dtype=np.float64)
        check = np.ones((10,1), dtype=int)

        myCrossover = Crossover.Crossover([])
        single_point_split_params = {'int_flag': True}
        children = myCrossover.single_point_split(array1, array2, single_point_split_params)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

        np.testing.assert_string_equal(str((children[0]).dtype), str(check.dtype))
        np.testing.assert_string_equal(str((children[1]).dtype), str(check.dtype))

class TestCrossoverPaul(unittest.TestCase):
    def testZeros(self):
        truss_1 = np.zeros(10, dtype=int)
        truss_2 = np.zeros(10, dtype=int)

        my_uniform_crossover = Crossover.Crossover([])
        result = my_uniform_crossover.uniform_crossover(truss_1, truss_2)

        np.testing.assert_array_equal(result[0], truss_1)
        np.testing.assert_array_equal(result[1], truss_2)

    def testOutputTypeInt(self):
        truss_1 = np.zeros(10, dtype=np.float64)
        truss_2 = np.zeros(10, dtype=np.float64)
        check = np.zeros(10, dtype=int)
        crossover_params = {'int_flag': True}

        my_uniform_crossover = Crossover.Crossover([])
        result = my_uniform_crossover.uniform_crossover(truss_1, truss_2, crossover_params)

        np.testing.assert_array_equal(result[0], check)
        np.testing.assert_array_equal(result[1], check)

        np.testing.assert_string_equal(str((result[0]).dtype), str(check.dtype))
        np.testing.assert_string_equal(str((result[1]).dtype), str(check.dtype))

class TestCrossover_twopointssplit(unittest.TestCase): #Amlan
    def test_sanity(self):

        array1 = np.ones((10,1))
        array2 = np.ones((10,1))
        check = np.ones((10,1))

        myCrossover = Crossover.Crossover([])
        children = myCrossover.two_points_split(array1, array2)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

    def test_datatype(self):

        array1 = np.ones((10,1), dtype=np.float64)
        array2 = np.ones((10,1), dtype=np.float64)
        check = np.ones((10,1), dtype=int)

        myCrossover = Crossover.Crossover([])
        two_points_split_params = {'int_flag': True}
        children = myCrossover.two_points_split(array1, array2, two_points_split_params)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

        np.testing.assert_string_equal(str((children[0]).dtype), str(check.dtype))
        np.testing.assert_string_equal(str((children[1]).dtype), str(check.dtype))

if __name__ == "__main__":
    unittest.main()
