#!/usr/bin/env python3

import numpy as np
import Truss
import unittest
import Eval
import Boundaries
import utilities


class TestEval(unittest.TestCase):

    def test_straight_beam(self):
        p = 10000  # load in newtons
        L = 4  # length in meters
        matl = 0
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0], [L, 0, 0]])
        edges = np.array([[0, 1]])
        properties = np.array([matl])
        truss = Truss.Truss(rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])
        load = np.array([[0, 0, 0, 0, 0, 0], [p, 0, 0, 0, 0, 0]])
        beam_dict = utilities.beam_file_parser('properties.csv')
        bdry = Boundaries.Boundaries(user_spec_nodes, load, dof)
        evaluator = Eval.Eval('mat_struct_analysis_DSM',
                              'mass_basic', None, bdry, beam_dict)
        evaluator(truss)
        A = beam_dict['x_section_area'][matl]
        E = beam_dict['elastic_modulus'][matl]
        sigma = p/A
        fos_true = beam_dict['yield_strength'][matl]/sigma
        epsilon = sigma/E
        deflection_true = np.array([[[0], [0], [0], [0], [0], [0]],
                                    [[epsilon*L], [0], [0], [0], [0], [0]]])

        np.testing.assert_almost_equal(
            truss.mass, A*L*beam_dict['density'][matl])
        np.testing.assert_array_almost_equal(truss.fos, fos_true)
        np.testing.assert_array_almost_equal(truss.deflection, deflection_true)


if __name__ == '__main__':
    unittest.main()
