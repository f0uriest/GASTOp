"""test_fitness.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the fitness class

"""
#!/usr/bin/env python3
import numpy as np
import unittest
from gastop import FitnessFunction, Truss


class TestFitness(unittest.TestCase):
    """Test cases for fitness functions"""

    def test_weighted_sum(self):
        """Tests weighted sum to make sure weights are implemented correctly"""

        fitness_params = {'goal_fos': 1.5,
                          'critical_nodes': np.array([1]),
                          'w_fos': 100,
                          'w_mass': 1,
                          'w_deflection': 10}
        f = FitnessFunction('weighted_sum', fitness_params)
        mass = 5
        deflection = np.array(
            [[1, 0, 0, 0, 0, 0], [np.sqrt(2), np.sqrt(2), 0, 0, 0, 0]])
        fos = np.array([.5, 5])
        t1 = Truss(0, 0, 0, 0)
        t1.mass = mass
        t1.deflection = deflection
        t1.fos = fos
        t1 = f(t1)
        self.assertAlmostEqual(t1.fitness_score, 125)

        t0 = Truss(0, 0, 0, 0)
        fitness_params['critical_nodes'] = np.array([])
        fos = np.array([])
        t0.mass = mass
        t0.deflection = deflection
        t0.fos = fos
        t0 = f(t0)
        self.assertAlmostEqual(t0.fitness_score, 185)

    def test_sphere(self):
        """Tests to make sure min is where it should be."""

        x = np.zeros(10)
        y = np.ones(10)
        t0 = Truss(x, x, 0, 0)
        t1 = Truss(y, y, 0, 0)
        f = FitnessFunction('sphere', {})
        t0 = f(t0)
        t1 = f(t1)
        self.assertAlmostEqual(t0.fitness_score, 0)
        self.assertAlmostEqual(t1.fitness_score, 10)

    def test_rosenbrock(self):
        """Tests to make sure min for rosenbrock function
        is where it should be.
        """

        x = np.zeros(11)
        y = np.ones(11)
        t0 = Truss(x, x, 0, 0)
        t1 = Truss(y, y, 0, 0)
        f = FitnessFunction('rosenbrock', {})
        t0 = f(t0)
        t1 = f(t1)
        self.assertAlmostEqual(t0.fitness_score, 5)
        self.assertAlmostEqual(t1.fitness_score, 0)

    def test_rastrigin(self):
        """Tests to make sure min for rastrigin function
        is where it should be.
        """

        x = np.zeros(10)
        y = np.ones(10)
        t0 = Truss(x, x, 0, 0)
        t1 = Truss(y, y, 0, 0)
        f = FitnessFunction('rastrigin', {})
        t0 = f(t0)
        t1 = f(t1)
        self.assertAlmostEqual(t0.fitness_score, 0)
        self.assertAlmostEqual(t1.fitness_score, 10)


if __name__ == '__main__':
    unittest.main()
