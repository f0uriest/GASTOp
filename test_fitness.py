import FitnessFunction
import Truss
import numpy as np
import unittest


class TestFitness(unittest.TestCase):

    def test_sphere(self):
        x = np.zeros(10)
        y = np.ones(10)
        t0 = Truss.Truss(x, 0, 0)
        t1 = Truss.Truss(y, 0, 0)
        f = FitnessFunction.FitnessFunction('sphere', 0)
        f(t0)
        f(t1)
        self.assertAlmostEqual(t0.fitness_score, 0)
        self.assertAlmostEqual(t1.fitness_score, 10)

    def test_rosenbrock(self):
        x = np.zeros(10)
        y = np.ones(10)
        t0 = Truss.Truss(x, 0, 0)
        t1 = Truss.Truss(y, 0, 0)
        f = FitnessFunction.FitnessFunction('rosenbrock', 0)
        f(t0)
        f(t1)
        self.assertAlmostEqual(t0.fitness_score, 5)
        self.assertAlmostEqual(t1.fitness_score, 0)

    def test_rastrigin(self):
        x = np.zeros(10)
        y = np.ones(10)
        t0 = Truss.Truss(x, 0, 0)
        t1 = Truss.Truss(y, 0, 0)
        f = FitnessFunction.FitnessFunction('rastrigin', 0)
        f(t0)
        f(t1)
        self.assertAlmostEqual(t0.fitness_score, 0)
        self.assertAlmostEqual(t1.fitness_score, 10)


if __name__ == '__main__':
    unittest.main()
