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

General
=======
:code:`[general]` contains the following parameters:

:user_spec_nodes: User-specified nodes (nodes with provided loads and displacement boundary conditions) as an nx3 numpy array of floats in the format :code:`'[[x1 y1 z1],[x2 y2 z2],...,[xn yn zn]]'`.

:loads: The forces and moments acting on each user-specified node as an nx6 numpy array of floats in the format :code:`'[[Fx1,Fy1,Fz1,Mx1,My1,Mz1],[Fx2,Fy2,Fz2,Mx2,My2,Mz2],...,[Fxn,Fyn,Fzn,Mxn,Myn,Mzn]]'`.

:fixtures: The translational and rotational displacements for each user-specified node as an nx6 numpy array of integers in the format :code:`'[[transx1,transy1,transz1,rotx1,roty1,rotz1],[transx2,transy2,transz2,rotx2,roty2,rotz2],...,[transxn,transyn,transzn,rotxn,rotyn,rotzn]]'`. Here :code:`transx1` is the translational degree of freedom in the x direction of the first user-specified node, and :code:`rotx1` is the rotational degree of freedom about the x-axis of the first user-specified node. A :code:`1` indicates fixed, while a :code:`0` indicates the node is free to move along or about the corresponding degree of freedom.

:num_rand_nodes: Maximum number of random nodes as an integer.

:num_rand_edges: Maximum number of random edges as an integer.

:properties_path: Path to the properties CSV as a string. For example, :code:`gastop-config/properties.csv`.

:domain: Allowable domain as a 3x2 numpy array of floats in the format :code:`'[[xmin xmax],[ymin ymax],[zmin zmax]]'`.

Fitness Function Parameters
===========================
:code:`[fitness_params]` contains the following parameters:

:equation: Method for calculating fitness as a string. *Options: weighted_sum, sphere, rosenbrock, rastrigin.*
:parameters:
       goal_fos: 4
       critical_nodes  '[3]'
       w_fos = 10000
       w_mass = 1
       w_deflection = 100

Evaluator Parameters
====================
:code:`[evaluator_params]` contains the following parameters:

:struct_solver: Method for solving truss as a string. *Options: mat_struct_analysis_DSM* *Default: mat_struct_analysis_DSM*
:mass_solver: Method of calculating the mass of a truss as a string. *Options: mass_basic* *Default: mass_basic*
:interferences_solver: Method of determining interferences as a string. *Options: blank_test, interference_ray_tracing* *Default: blank_test*
:cost_solver: Method of calculating the cost of a truss as a string. *Options: cost_calc* *Default: cost_calc*

Genetic Algorithm Parameters
============================
:code:`[ga_params]` contains the following parameters:

:num_threads: Number of threads as an integer. If equal to one, the GenAlg.run() method will execute in serial. If greater than one, it will run in parallel.
:pop_size: Number of trusses in each generation as an integer.
:num_generations: Number of generations to run as an integer.
:num_elite: Number of fittest trusses to carry over to the next generation without modification as an integer.
:percent_mutation: Percent of trusses in the next generation (after subtracting elites) to be derived from mutation of current trusses as a float.
:percent_crossover: Percent of trusses in the next generation (after subtracting elites) to be derived from crossover of current trusses as a float.
:save_frequency: Number of generations after which the population and config are saved to .json files as an integer.
:save_filename_prefix: Prefix for the save filenames as a string. For example, :code:`save_`.

Progress Monitor Parameters
===========================
:code:`[monitor_params]` contains the following parameters:

:progress_display: Progress monitor display mode as a string. *Options: ...*




Advanced Parameters
*******************

Random Generation Parameters
============================
:code:`[random_params]` contains the following parameters:


Crossover Parameters
====================
:code:`[crossover_params]` contains the following parameters:

:node_crossover_method: Method for performing node crossover as a string. *Options: uniform_crossover, single_point_split, two_points_split* *Default: uniform_crossover*
:edge_crossover_method: Method for performing edge crossover as a string. *Options: uniform_crossover, single_point_split, two_points_split* *Default: uniform_crossover*
:property_crossover_method: Method for performing edge crossover as a string. *Options: uniform_crossover, single_point_split, two_points_split* *Default: uniform_crossover*
:node_crossover_params: Dictionary of additional node crossover parameters.
:edge_crossover_params: Dictionary of additional edge crossover parameters.
:property_crossover_params: Dictionary of additional property crossover parameters.

Mutator Parameters
==================
:code:`[mutator_params]` contains the following parameters:

:node_mutator_method: Method for performing node mutation as a string. *Options: gaussian, pseudo_bit_flip, shuffle_index* *Default: gaussian*
:edge_mutator_method: Method for performing edge mutation as a string. *Options: gaussian, pseudo_bit_flip, shuffle_index* *Default: pseudo_bit_flip*
:property_mutator_method: Method for performing property mutation as a string. *Options: gaussian, pseudo_bit_flip, shuffle_index* *Default: pseudo_bit_flip*
      [[node_mutator_params]]
      std =
      [[edge_mutator_params]]
      proportions =
      [[property_mutator_params]]
      proportions =
      
Selector Parameters
===================
:code:`[selector_params]` contains the following parameters:

:method: Method for performing selection as a string. *Options: inverse_square_rank_probability, tournament* *Default: inverse_square_rank_probability*
:tourn_size: The number of truss indices in each tournament as an integer. Must be less than 32.
:tourn_prob: The probability of the fittest truss in a tournamment to be selected as a float.
