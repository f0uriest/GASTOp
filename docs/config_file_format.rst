==================================
Config File Formatting and Options
==================================

The config file includes all the input parameters used to instantiate a
GenAlg() object. Certain parameters must be specified by the user, while other
more advanced parameters can be left blank for simplicity and will default to
reasonable values.

The config file is parsed as a nested dictionary, where each dictionary is
indicated by :code:`[dict]` for a value at the highest level, and nested
dictionaries are indicated by nested squared brackets, :code:`[[nested dict]]`.
Each dictionary contains multiple arguments indicated by :code:`key: value`.
If the value is an integer, float, or string, simply input the value without
quotation marks. If the value is a numpy array, input the value as a the
array in list format, within single quotes, like :code:`key: '[[0 1],[3 2]]'`.

Required Parameters
*******************

General
=======
Under :code:`[general]` there are multiple variable

:what: user_spec_nodes = '[[0,-.5,0],[0,.5,0],[0,0,1],[2,0,0]]'
:how:

:what: loads = '[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,-10000,0,0,0]]'
:how:

:what: fixtures = '[[1,1,1,0,0,0],[1,1,1,0,0,0],[1,1,1,0,0,0],[0,0,0,0,0,0]]'
:how:

:what: num_rand_nodes = 10 # int
:how:

:what: num_rand_edges = 10 # int
:how:

:what: properties_path = 'gastop-config/properties.csv'
:how:

:what: domain = '[[-1, -1, -1], [5, 1, 2]]'
:how:

[fitness_params]
equation = weighted_sum
       [[parameters]]
       goal_fos = 4
       critical_nodes = '[3]'
       w_fos = 10000
       w_mass = 1
       w_deflection = 100

[evaluator_params]
struct_solver = mat_struct_analysis_DSM
mass_solver = mass_basic
interferences_solver = blank_test
cost_solver = cost_calc

[ga_params]
num_threads = 4
pop_size = 1000
num_generations = 30
num_elite =
percent_mutation =
percent_crossover =
save_frequency = 5
save_filename_prefix = Recorded_States_

[monitor_params]
progress_display = 1

Advanced Parameters
*******************

explain different headings and options, with references to API docs


[random_params]


[crossover_params]
node_crossover_method =
edge_crossover_method =
property_crossover_method =
      [[node_crossover_params]]
      [[edge_crossover_params]]
      [[property_crossover_params]]


[mutator_params]
node_mutator_method =
edge_mutator_method =
property_mutator_method =
      [[node_mutator_params]]
      std =
      [[edge_mutator_params]]
      proportions =
      [[property_mutator_params]]
      proportions =

[selector_params]
method =
tourn_size = 31 # Must be less than 32
tourn_prob = 0.5
