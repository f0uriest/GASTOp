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

:equation: = weighted_sum
       [[parameters]]
       goal_fos = 4
       critical_nodes = '[3]'
       w_fos = 10000
       w_mass = 1
       w_deflection = 100

Evaluator Parameters
====================
:code:`[evaluator_params]` contains the following parameters:

:struct_solver: = mat_struct_analysis_DSM
:mass_solver: = mass_basic
:interferences_solver: = blank_test
:cost_solver: = cost_calc

Genetic Algorithm Parameters
============================
:code:`[ga_params]` contains the following parameters:

:num_threads: = 4
:pop_size: = 1000
:num_generations: = 30
:num_elite: =
:percent_mutation: =
:percent_crossover: =
:save_frequency: = 5
:save_filename_prefix: = Recorded_States_

Progress Monitor Parameters
===========================
:code:`[monitor_params]` contains the following parameters:

:progress_display: = 1


Advanced Parameters
*******************

explain different headings and options, with references to API docs

Random Generation Parameters
============================
:code:`[random_params]` contains the following parameters:


Crossover Parameters
====================
:code:`[crossover_params]` contains the following parameters:

:node_crossover_method: =
:edge_crossover_method: =
:property_crossover_method: =
      [[node_crossover_params]]
      [[edge_crossover_params]]
      [[property_crossover_params]]

Mutator Parameters
==================
:code:`[mutator_params]` contains the following parameters:

:node_mutator_method: =
:edge_mutator_method: =
:property_mutator_method: =
      [[node_mutator_params]]
      std =
      [[edge_mutator_params]]
      proportions =
      [[property_mutator_params]]
      proportions =
      
Selector Parameters
===================
:code:`[selector_params]` contains the following parameters:

:method: =
:tourn_size: = 31 # Must be less than 32
:tourn_prob: = 0.5
