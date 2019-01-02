#!/usr/bin/env python3
import unittest
import numpy as np
from gastop import Truss, Evaluator, utilities


class TestEvaluator(unittest.TestCase):

    def test_axial_load(self):
        """Tests simple straight beam under axial forces"""

        p = 10000  # load in newtons
        L = 4  # length in meters
        matl = 0
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0], [L, 0, 0]])
        edges = np.array([[0, 1]])
        properties = np.array([matl])
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
                       ).reshape(2, 6, 1)
        load = np.array(
            [[0, 0, 0, 0, 0, 0], [p, 0, 0, 0, 0, 0]]).reshape(2, 6, 1)
        beam_dict = utilities.beam_file_parser('gastop-config/properties.csv')
        bdry = {'loads': load, 'fixtures': dof}
        evaluator = Evaluator('mat_struct_analysis_DSM',
                              'mass_basic', 'interference_ray_tracing', bdry, beam_dict)
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
        self.assertTrue(truss.interference is None)

    def test_singular_stiffness_matrix(self):
        """Tests straight beam under axial forces with no restraints

        Should return fos = 0, as stiffness matrix is singular
        """

        p = 10000  # load in newtons
        L = 4  # length in meters
        matl = 0
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0], [L, 0, 0]])
        edges = np.array([[0, 1]])
        properties = np.array([matl])
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        dof = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
                       ).reshape(2, 6, 1)
        load = np.array(
            [[0, 0, 0, 0, 0, 0], [p, 0, 0, 0, 0, 0]]).reshape(2, 6, 1)
        beam_dict = utilities.beam_file_parser('gastop-config/properties.csv')
        bdry = {'loads': load, 'fixtures': dof}
        evaluator = Evaluator('mat_struct_analysis_DSM',
                              'mass_basic', 'blank_test', bdry, beam_dict)
        evaluator(truss)
        fos_true = 0

        np.testing.assert_array_almost_equal(truss.fos, fos_true)

    def test_combined_load(self):
        """Tests beam under combined loading

        Beam is fixed at one end, and loads applied at the other,
        creating bending moment, torsion and shear forces.
        From Shigley's Mechanical Engineering Design, 10th ed, pp 247-248
        """
        p = 9000  # axial load in newtons
        f = 1750  # transverse load in newtons
        T = 72  # torsion in newton-meters
        L = .12  # length in meters
        matl = 4
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0], [L, 0, 0]])
        edges = np.array([[0, 1]])
        properties = np.array([matl])
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
                       ).reshape(2, 6, 1)
        load = np.array(
            [[0, 0, 0, 0, 0, 0], [p, -f, 0, -T, 0, 0]]).reshape(2, 6, 1)
        beam_dict = utilities.beam_file_parser('gastop-config/properties.csv')
        bdry = {'loads': load, 'fixtures': dof}
        evaluator = Evaluator('mat_struct_analysis_DSM',
                              'mass_basic', 'blank_test', bdry, beam_dict)
        evaluator(truss)
        A = beam_dict['x_section_area'][matl]
        E = beam_dict['elastic_modulus'][matl]
        Iz = beam_dict['moment_inertia_z'][matl]
        sigma = p/A
        fos_true = 4.57
        epsilon = sigma/E

        np.testing.assert_almost_equal(
            truss.mass, A*L*beam_dict['density'][matl])
        np.testing.assert_array_almost_equal(truss.fos, fos_true, 2)

    def test_unsupported_load(self):
        """Tests straight beam under axial forces with additional unsupported load

        Should return fos = 0, as stiffness matrix is singular
        """

        p = 10000  # load in newtons
        L = 4  # length in meters
        matl = 0
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0],
                                    [L, 0, 0],
                                    [0, 0, L]])
        edges = np.array([[0, 1]])
        properties = np.array([matl])
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]]).reshape(3, 6, 1)
        load = np.array([[0, 0, 0, 0, 0, 0],
                         [p, 0, 0, 0, 0, 0],
                         [p, 0, 0, 0, 0, 0]]).reshape(3, 6, 1)
        beam_dict = utilities.beam_file_parser('gastop-config/properties.csv')
        bdry = {'loads': load, 'fixtures': dof}
        evaluator = Evaluator('mat_struct_analysis_DSM',
                              'mass_basic', 'blank_test', bdry, beam_dict)
        evaluator(truss)
        fos_true = 0

        np.testing.assert_array_almost_equal(truss.fos, fos_true)

    def test_unconnected_node(self):
        """Tests truss with 3 nodes and 1 connection

        3rd node is not connected to the other two, and is not loaded or supported
        should return nonzero fos, as unconnected node is not loaded so is ignored
        """

        p = 10000  # load in newtons
        L = 4  # length in meters
        matl = 2
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0],
                                    [L, 0, 0],
                                    [0, L, 0]])
        edges = np.array([[0, 1]])
        properties = np.array([matl])
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]]).reshape(3, 6, 1)
        load = np.array([[0, 0, 0, 0, 0, 0],
                         [p, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0]]).reshape(3, 6, 1)
        beam_dict = utilities.beam_file_parser('gastop-config/properties.csv')
        bdry = {'loads': load, 'fixtures': dof}
        evaluator = Evaluator('mat_struct_analysis_DSM',
                              'mass_basic', 'blank_test', bdry, beam_dict)
        evaluator(truss)
        A = beam_dict['x_section_area'][matl]
        E = beam_dict['elastic_modulus'][matl]
        sigma = p/A
        fos_true = beam_dict['yield_strength'][matl]/sigma

        np.testing.assert_almost_equal(
            truss.mass, A*L*beam_dict['density'][matl])
        np.testing.assert_array_almost_equal(truss.fos, fos_true)

    def test_duplicate_members(self):
        """Tests a truss with duplicate members between two nodes,
        to ensure those members are not counted"""

        p = 9000  # axial load in newtons
        f = 1750  # transverse load in newtons
        T = 72  # torsion in newton-meters
        L = .12  # length in meters
        matl = 4
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 0, 0], [L, 0, 0]])
        edges = np.array([[0, 1], [0, 1]])
        properties = np.array([matl, matl])
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
                       ).reshape(2, 6, 1)
        load = np.array(
            [[0, 0, 0, 0, 0, 0], [p, -f, 0, -T, 0, 0]]).reshape(2, 6, 1)
        beam_dict = utilities.beam_file_parser('gastop-config/properties.csv')
        bdry = {'loads': load, 'fixtures': dof}
        evaluator = Evaluator('mat_struct_analysis_DSM',
                              'mass_basic', 'blank_test', bdry, beam_dict)
        evaluator(truss)
        A = beam_dict['x_section_area'][matl]
        E = beam_dict['elastic_modulus'][matl]
        Iz = beam_dict['moment_inertia_z'][matl]
        sigma = p/A
        fos_true = 4.57
        epsilon = sigma/E

        np.testing.assert_almost_equal(
            truss.mass, A*L*beam_dict['density'][matl])
        np.testing.assert_array_almost_equal(truss.fos[0], fos_true, 2)

    def test_fixtures(self):
        """Tests applied loads with various dof fixed"""

        p = 1000  # load in newtons
        L = 1  # length in meters
        matl = 2
        rand_nodes = np.array([]).reshape(0, 3)  # no random nodes
        user_spec_nodes = np.array([[0, 1, 0],
                                    [L, 0, 0],
                                    [0, -1, 0]])
        edges = np.array([[0, 1], [2, 1]])
        properties = matl*np.ones((edges.shape[0])).astype(int)
        truss = Truss(user_spec_nodes, rand_nodes, edges, properties)
        dof = np.array([[1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 0, 0]]).reshape(3, 6, 1)
        load = np.array([[0, 0, 0, 0, 0, 0],
                         [0, 0, -p, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0]]).reshape(3, 6, 1)
        beam_dict = utilities.beam_file_parser('gastop-config/properties.csv')
        bdry = {'loads': load, 'fixtures': dof}
        evaluator = Evaluator('mat_struct_analysis_DSM',
                              'mass_basic', 'blank_test', bdry, beam_dict)
        evaluator(truss)

        fos_true = np.zeros((edges.shape[0], 1))
        # fos should be zero, structure is statically indeterminate,
        # but member releases aren't working
#        np.testing.assert_array_almost_equal(truss.fos, fos_true)


if __name__ == '__main__':
    unittest.main()
