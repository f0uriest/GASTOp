"""test_crossover.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the crossover class

"""
#!/usr/bin/env python3

import unittest
import numpy as np

from gastop import Crossover


class TestCrossover_singlepointsplit(unittest.TestCase):  # Amlan

    def test_sanity(self):

        array1 = np.ones((10, 1))
        array2 = np.ones((10, 1))
        check = np.ones((10, 1))

        children = Crossover.single_point_split(array1, array2)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

    def test_datatype(self):

        array1 = np.ones((10, 1), dtype=int)
        array2 = np.ones((10, 1), dtype=int)
        check = np.ones((10, 1), dtype=int)

        children = Crossover.single_point_split(array1, array2)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

        np.testing.assert_string_equal(
            str((children[0]).dtype), str(check.dtype))
        np.testing.assert_string_equal(
            str((children[1]).dtype), str(check.dtype))


class TestCrossoverPaul(unittest.TestCase):
    def testZeros(self):
        truss_1 = np.zeros(10, dtype=int)
        truss_2 = np.zeros(10, dtype=int)

        result = Crossover.uniform_crossover(truss_1, truss_2)

        np.testing.assert_array_equal(result[0], truss_1)
        np.testing.assert_array_equal(result[1], truss_2)

    def testOutputTypeInt(self):
        truss_1 = np.zeros(10, dtype=int)
        truss_2 = np.zeros(10, dtype=int)
        check = np.zeros(10, dtype=int)

        result = Crossover.uniform_crossover(truss_1, truss_2)

        np.testing.assert_array_equal(result[0], check)
        np.testing.assert_array_equal(result[1], check)

        np.testing.assert_string_equal(
            str((result[0]).dtype), str(check.dtype))
        np.testing.assert_string_equal(
            str((result[1]).dtype), str(check.dtype))

    def testChildInParents(self):
        truss_1 = np.random.randint(10, size=25)
        truss_2 = np.random.randint(10, size=25)
        parents_combined = np.concatenate((truss_1, truss_2))

        result = Crossover.uniform_crossover(truss_1, truss_2)

        child1_status = str(np.all(np.in1d(result[0],
                                           parents_combined)))
        child2_status = str(np.all(np.in1d(result[1],
                                           parents_combined)))

        np.testing.assert_string_equal(child1_status, str(True))
        np.testing.assert_string_equal(child2_status, str(True))


class TestCrossover_twopointssplit(unittest.TestCase):  # Amlan
    def test_sanity(self):

        array1 = np.ones((10, 1))
        array2 = np.ones((10, 1))
        check = np.ones((10, 1))

        children = Crossover.two_points_split(array1, array2)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

    def test_datatype(self):

        array1 = np.ones((10, 1), dtype=np.float64)
        array2 = np.ones((10, 1), dtype=np.float64)
        check = np.ones((10, 1), dtype=np.float64)

        children = Crossover.two_points_split(array1, array2)

        np.testing.assert_array_equal(children[0], check)
        np.testing.assert_array_equal(children[1], check)

        np.testing.assert_string_equal(
            str((children[0]).dtype), str(check.dtype))
        np.testing.assert_string_equal(
            str((children[1]).dtype), str(check.dtype))


if __name__ == "__main__":
    unittest.main()
