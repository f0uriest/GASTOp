"""test_basic_optimization.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for basic optimization

"""
#!/usr/bin/env python3

import unittest
import numpy as np
from gastop import GenAlg

ga_params = {
    # ga_params
    'pop_size': 1000,
    'num_generations': 100,
    'num_threads': None,
    'num_elite': 10,  # int, ~10 (the whole truss that get passed)
    'percent_crossover': 0.4,  # double between 0 and 1
    'percent_mutation': 0.4,  # double between 0 and 1
    'save_frequency': 0,
    'save_filename_prefix': 'Recorded_States_'

}

random_params = {
    # Random
    'num_rand_nodes': 2,  # int
    'num_rand_edges': 10,  # int
    # np array 2x3 [[xmin,ymin,zmin],[xmax,ymax,zmax]]
    'domain': np.array([[-5, -5, -5], [5, 5, 5]]),
    'num_material_options': 10,
    'user_spec_nodes': np.array([[]]).reshape(0, 3),
    'rng_seed': 0
}

crossover_params = {
    'node_crossover_method': 'uniform_crossover',
    'edge_crossover_method': 'uniform_crossover',
    'property_crossover_method': 'single_point_split',
    'node_crossover_params': {},
    'edge_crossover_params': {},
    'property_crossover_params': {},
    'user_spec_nodes': np.array([[]]).reshape(0, 3)

}

mutator_params = {
    'node_mutator_method': 'gaussian',
    'edge_mutator_method': 'pseudo_bit_flip',
    'property_mutator_method': 'gaussian',

    'node_mutator_params': {'std': 0.01, 'boundaries': np.array([[-5, -5, -5], [5, 5, 5]]), 'int_flag': False},
    'edge_mutator_params': {'boundaries': np.array([[-1, -1], [10, 10]]), 'proportions': 0.5, 'int_flag': False},
    'property_mutator_params': {'std': 2, 'boundaries': np.array([[-1], [10]]), 'int_flag': False},
    'user_spec_nodes': np.array([[]]).reshape(0, 3)

}

selector_params = {
    'method': 'inverse_square_rank_probability', 'method_params': {}}
evaluator_params = {'struct_solver': 'blank_test',
                    'mass_solver': 'blank_test',
                    'interferences_solver': 'blank_test',
                    'boundary_conditions': {'loads': 0, 'fixtures': 0, },
                    'properties_dict': 0,
                    'cost_solver': 'blank_test'}
monitor_params = {'progress_fitness': False,
                  'progress_truss': False}

config = {'ga_params': ga_params,
          'random_params': random_params,
          'mutator_params': mutator_params,
          'crossover_params': crossover_params,
          'selector_params': selector_params,
          'evaluator_params': evaluator_params,
          'monitor_params': monitor_params}

pop_size = 1000


class TestOptimization(unittest.TestCase):
    """Tests genetic algorithm's ability to solve basic 
    convex and non-convex test cases.
    """

    def test_rastrigin(self):
        """Test GA using rastrigin function,
        highly non-convex optimization test function.
        """

        config['fitness_params'] = {
            'equation': 'rastrigin', 'parameters': {}}
        config['ga_params']['pop_size'] = 1000
        ga = GenAlg(config)
        ga.initialize_population()
        best, progress_history = ga.run()
        self.assertAlmostEqual(best.fitness_score, 0, places=2)

    def test_sphere(self):
        """Tests GA using sphere function, 
        ie sum of squares. Simple convex test case.
        """

        config['ga_params']['num_threads'] = 2
        config['fitness_params'] = {'equation': 'sphere', 'parameters': {}}
        ga = GenAlg(config)
        ga.initialize_population(pop_size)
        best, progress_history = ga.run(
            num_generations=100, progress_fitness=True, progress_truss=False)
        self.assertAlmostEqual(best.fitness_score, 0, places=4)


if __name__ == '__main__':
    unittest.main()
