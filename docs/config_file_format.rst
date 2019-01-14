==================================
Config File Formatting and Options
==================================

The config file includes all the input parameters used to instantiate a
GenAlg() object. Certain parameters must be specified by the user, while other
more advanced parameters can be left blank for simplicity and will default to
reasonable values.

The config file is parsed as a nested dictionary. Each dictionary is
indicated by :code:`[dict]`, and nested dictionaries are indicated by nested
squared brackets, :code:`[[nested dict]]`. Each dictionary contains multiple
arguments indicated by :code:`key: value`. If the value is an integer, float,
or string, simply input the value without quotation marks. For instance,
:code:`key: 3`, :code:`key: 3.14`, or :code:`key: pi`. If the value
is a numpy array, input the value as an array in list format, within single
quotes, like :code:`key: '[[3.14 3.14],[3.14 3.14]]'`.

For instance, the config file:

.. code-block:: python

       [dict1]
       key1: 3
       key2: 3.14
       [[sub_dict1]]
       sub_key1: apples
       [[sub_dict2]]
       sub_key2: None
       [dict2]
       key3: '[[3.14 12.8],[6.7 88.9999]]'


would be parsed, forming the dictionary:

.. code-block:: python

       {'dict1':
              {'key1':3,
              'key2':3.14,
              'sub_dict1':{'sub_key1':'apples'},
              'sub_dict2':{'sub_key2':None}},
        'dict2':
              {'key3':array([[3.14 12.8],[6.7 88.9999]])}}


Required Parameters
*******************

General Parameters
==================
:code:`[general]` contains the following parameters:

:user_spec_nodes: **(nx3 numpy array of floats)** User-specified nodes (nodes with provided loads and displacement boundary conditions) in the format :code:`'[[x1 y1 z1],[x2 y2 z2],...,[xn yn zn]]'`.

:loads: **(nx6 numpy array of floats)** The forces and moments acting on each user-specified node in the format :code:`'[[Fx1,Fy1,Fz1,Mx1,My1,Mz1][Fx2,Fy2,Fz2,Mx2,My2,Mz2],...,[Fxn,Fyn,Fzn,Mxn,Myn,Mzn]]'`.

:fixtures: **(nx6 numpy array of ints)** The translational and rotational displacements for each user-specified node in the format :code:`'[[transx1,transy1,transz1,rotx1,roty1,rotz1],[transx2,transy2,transz2,rotx2,roty2,rotz2],...,[transxn,transyn,transzn,rotxn,rotyn,rotzn]]'`. Here :code:`transx1` is the translational degree of freedom in the x direction of the first user-specified node, and :code:`rotx1` is the rotational degree of freedom about the x-axis of the first user-specified node. A :code:`1` indicates fixed, while a :code:`0` indicates the node is free to move along or about the corresponding degree of freedom.

:num_rand_nodes: **(int)** Maximum number of random nodes.

:num_rand_edges: **(int)** Maximum number of random edges.

:properties_path: **(str)** Path to the properties CSV. For example, :code:`gastop-config/properties.csv`.

:domain: **(3x2 numpy array of floats)** Allowable domain in the format :code:`'[[xmin xmax],[ymin ymax],[zmin zmax]]'`.

Fitness Function Parameters
===========================
:code:`[fitness_params]` contains the following parameters (see fitness_function_):

.. _fitness_function: https://gastop.readthedocs.io/en/latest/api.html#fitnessfunction

:equation: **(str)** Method for calculating fitness. *Options: weighted_sum, sphere, rosenbrock, rastrigin.*
:parameters: **(dict)** Additional fitness function parameters.
:parameters['goal_fos']: **(int)** Desired factor of safety.
:parameters['critical_nodes']: **(1xn numpy array of ints)** Array of nodes numbers for which deflection should be minimized. If empty, defaults to all.
:parameters['w_fos']: **(float)** Penalty weight for low fos. Only applied if truss.fos < *goal_fos*.
:parameters['w_mass']: **(float)** Penalty applied to mass. Relative magnitude of *w_mass* and *w_fos* determines importance of minimizing mass vs maximizing fos.
:parameters['w_deflection']: **(float)** Penalty applied to deflections.
                  If scalar, applies the same penalty to all critical nodes.
                  Can also be an array the same size as *critical_nodes* in
                  which case different penalties will be applied to each node.

Evaluator Parameters
====================
:code:`[evaluator_params]` contains the following parameters (see evaluator_):

.. _evaluator: https://gastop.readthedocs.io/en/latest/api.html#evaluator

:struct_solver: **(str)** Method for solving truss. *Options: mat_struct_analysis_DSM* *Default: mat_struct_analysis_DSM*
:mass_solver: **(str)** Method of calculating the mass of a truss. *Options: mass_basic* *Default: mass_basic*
:interferences_solver: **(str)** Method of determining interferences. *Options: blank_test, interference_ray_tracing* *Default: blank_test*
:cost_solver: **(str)** Method of calculating the cost of a truss. *Options: cost_calc* *Default: cost_calc*

Genetic Algorithm Parameters
============================
:code:`[ga_params]` contains the following parameters (see gen_alg_):

.. _gen_alg: https://gastop.readthedocs.io/en/latest/api.html#genalg

:num_threads: **(int)** Number of threads. If equal to one, the GenAlg.run() method will execute in serial. If greater than one, it will run in parallel.
:pop_size: **(int)** Number of trusses in each generation.
:num_generations: **(int)** Number of generations to run.
:num_elite: **(int)** Number of fittest trusses to carry over to the next generation without modification.
:percent_mutation: **(float)** Percent of trusses in the next generation (after subtracting elites) to be derived from mutation of current trusses.
:percent_crossover: **(float)** Percent of trusses in the next generation (after subtracting elites) to be derived from crossover of current trusses.
:save_frequency: **(int)** Number of generations after which the population and config are saved to .json files.
:save_filename_prefix: **(str)** Prefix for the save filenames. For example, :code:`save_`.

Progress Monitor Parameters
===========================
:code:`[monitor_params]` contains the following parameters (see progress_monitor_):

.. _progress_monitor: https://gastop.readthedocs.io/en/latest/api.html#progress-monitor

:progress_fitness: **(bool)** Progress monitor display mode, if true displays best fitness score of the population each generation.
:progress_truss: **(bool)** Progress monitor display mode, if true displays the truss with the best fitness score each generation.  




Optional Parameters
*******************

Random Generation Parameters
============================
:code:`[random_params]` contains the following parameters:


Crossover Parameters
====================
:code:`[crossover_params]` contains the following parameters (see crossover_):

.. _crossover: https://gastop.readthedocs.io/en/latest/api.html#crossover

:node_crossover_method: **(str)** Method for performing node crossover. *Options: uniform_crossover, single_point_split, two_points_split* *Default: uniform_crossover*
:edge_crossover_method: **(str)** Method for performing edge crossover. *Options: uniform_crossover, single_point_split, two_points_split* *Default: uniform_crossover*
:property_crossover_method: **(str)** Method for performing edge crossover. *Options: uniform_crossover, single_point_split, two_points_split* *Default: uniform_crossover*
:node_crossover_params: **(dict)** Additional node crossover parameters.
:edge_crossover_params: **(dict)** Additional edge crossover parameters.
:property_crossover_params: **(dict)** Additional property crossover parameters.

Mutator Parameters
==================
:code:`[mutator_params]` contains the following parameters (see mutator_):

.. _mutator: https://gastop.readthedocs.io/en/latest/api.html#mutator

:node_mutator_method: **(str)** Method for performing node mutation. *Options: gaussian, pseudo_bit_flip, shuffle_index* *Default: gaussian*
:edge_mutator_method: **(str)** Method for performing edge mutation. *Options: gaussian, pseudo_bit_flip, shuffle_index* *Default: pseudo_bit_flip*
:property_mutator_method: **(str)** Method for performing property mutation. *Options: gaussian, pseudo_bit_flip, shuffle_index* *Default: pseudo_bit_flip*
:node_mutator_params: **(dict)** Additional node mutator parameters.
:node_mutator_params['std']: **(float)** Standard deviation for mutation. If array-like,
                std[i] is used as the standard deviation for array[:,i].
:edge_mutator_params: **(dict)** Additional edge mutator parameters.
:edge_mutator_params['proportions']: **(float)** Probability of a given entry being mutated.
:property_mutator_params: **(dict)** Additional property mutator parameters.
:property_mutator_params['proportions']: **(float)** Probability of a given entry being mutated.

Selector Parameters
===================
:code:`[selector_params]` contains the following parameters (see selector_):

.. _selector: https://gastop.readthedocs.io/en/latest/api.html#selector

:method: **(str)** Method for performing selection. *Options: inverse_square_rank_probability, tournament* *Default: inverse_square_rank_probability*
:tourn_size: **(int)** The number of truss indices in each tournament. Must be less than 32.
:tourn_prob: **(float)** The probability of the fittest truss in a tournament to be selected.

Properties Parsing
******************
While parsing the config file, GASTOp will read the path to a file that contains the user-specified property information from a CSV file. The file exists by default as :code:`properties.csv` with a few available material options:

..

+------+-------------+--------+--------+----------------------+---------------------+---------------+---------------+------+
| beam | material    | OD (m) | ID (m) | elastic_modulus (Pa) | yield_strength (Pa) | dens (kg/m^3) | poisson_ratio | cost |
+======+=============+========+========+======================+=====================+===============+===============+======+
| 0	| steel       | 0.025  | 0.02   |     200000000000     | 250000000	       | 8050	         | 0.3	    | 1    |
+------+-------------+--------+--------+----------------------+---------------------+---------------+---------------+------+
| 1	| steel	| 0.012  | 0.01   |     200000000000     | 250000000	       | 8050	         | 0.3	    | 0.75 |
+------+-------------+--------+--------+----------------------+---------------------+---------------+---------------+------+
| 2	| aluminum	| 0.025  | 0.02   |     69000000000      | 95000000	       | 2700	         | 0.32	    | 2    |
+------+-------------+--------+--------+----------------------+---------------------+---------------+---------------+------+
| 3	| aluminum	| 0.012  | 0.01   |     69000000000      | 95000000	       | 2700	         | 0.32	    | 1.5  |
+------+-------------+--------+--------+----------------------+---------------------+---------------+---------------+------+
| 4	| 2024 alum	| 0.042  | 0.032  |     69000000000      | 276000000	       | 2700	         | 0.32	    | 3    |
+------+-------------+--------+--------+----------------------+---------------------+---------------+---------------+------+

              
Adding additional materials is as simple as adding a row to the default file, with all values separated by commas. One could also alternatively create a new properties file, duplicating the format of the default, replacing all material data, and specifying the path to the new properties file in the config file.
