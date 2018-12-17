#!/usr/bin/env python3

import numpy as np
import Truss
import unittest
import Eval
import Boundaries
import utilities


class TestEval(unittest.TestCase):

    def test_straight_beam(self):
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0], [1, 0, 0]])
        edges = np.array([[0, 1]])
        properties = np.array([0])
        truss = Truss.Truss(rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])
        load = np.array([[0, 0, 0, 0, 0, 0], [1000, 0, 0, 0, 0, 0]])
        beam_dict = utilities.beam_file_parser('properties.csv')
        bdry = Boundaries.Boundaries(user_spec_nodes, load, dof)
        evaluator = Eval.Eval('mat_struct_analysis_DSM',
                              'mass_basic', None, bdry, beam_dict)
        evaluator(truss)
        print(truss.mass)
        print(truss.fos)
        print(truss.deflection)

        np.testing.assert_almost_equal(truss.mass, 1.42255242)


if __name__ == '__main__':
    unittest.main()
