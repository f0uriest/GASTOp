"""utilities.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the utilities class.

"""

import numpy as np
import configobj
import json
import ast
import os
import imageio
import matplotlib.pyplot as plt
import shutil

from gastop import Truss, ProgMon, encoders


def save_gif(progress_history, progress_fitness, progress_truss, animation_path, num_gens, config):

    # delete old animation folder
    try:
        # doesnt seem to be removing everything properly?
        shutil.rmtree(animation_path)
    except:
        pass
    os.makedirs(animation_path)

    if progress_fitness or progress_truss:
        evolution = ProgMon(progress_fitness, progress_truss, num_gens, config['random_params']['domain'],
                            config['evaluator_params']['boundary_conditions']['loads'],
                            config['evaluator_params']['boundary_conditions']['fixtures'])



        images = []
        for current_gen in range(num_gens):
            progress_truss = progress_history['Generation ' +
                                              str(current_gen+1)]['Best Truss']
            # progress_truss.plot(domain=config['random_params']['domain'],
            #          fixtures=config['evaluator_params']['boundary_conditions']['fixtures'])
            evolution.progress_monitor(current_gen, progress_truss)
            fig = plt.gcf()
            fig.savefig(animation_path + '/truss_evo_iter' +
                        str(current_gen+1) + '.png')
            images.append(imageio.imread(
                'animation/truss_evo_iter' + str(current_gen+1) + '.png'))
        imageio.mimsave(animation_path + '/truss_evo_gif.gif',
                        images, duration=0.5)

        progress_history['Generation 1']['Best Truss'].plot(domain=config['random_params']['domain'],
                   loads=config['evaluator_params']['boundary_conditions']['loads'],
                   fixtures=config['evaluator_params']['boundary_conditions']['fixtures'],
                   deflection=False,setup_only=True)
        fig2= plt.gcf()
        fig2.savefig(animation_path + '/simulation_setup.png')
        plt.close()


def beam_file_parser(properties_path):
    """Parses csv file of beam material properties

    Each line of the properties file denotes one type of beam, with a specified
    cross section and material properties.

    Property entries should be formatted as:
    beam #, material name, OD (m), ID (m), elastic_modulus (Pa),
    yield_strength (Pa), density (kg/m^3), poisson_ratio, cost

    Args:
        properties_path (str): Path to the properties csv file, relative to
            the directory GASTOp is being executed from.

    Returns:
        properties_dict (dict): Dictionary of property values.
        Each entry is an ndarray of the key property of each beam. For example,
        properties_dict['dens'] is an ndarray of the density of each beam.

    """

    OD = np.loadtxt(properties_path, delimiter=',', skiprows=1, usecols=2)
    ID = np.loadtxt(properties_path, delimiter=',', skiprows=1, usecols=3)
    E = np.loadtxt(properties_path, delimiter=',', skiprows=1, usecols=4)
    YS = np.loadtxt(properties_path, delimiter=',', skiprows=1, usecols=5)
    dens = np.loadtxt(properties_path, delimiter=',', skiprows=1, usecols=6)
    nu = np.loadtxt(properties_path, delimiter=',', skiprows=1, usecols=7)
    cost = np.loadtxt(properties_path, delimiter=',', skiprows=1, usecols=8)
    G = E/(2*(1+nu))
    A = np.pi/4*(OD**2 - ID**2)
    Iz = np.pi/64*(OD**4 - ID**4)
    Iy = np.pi/64*(OD**4 - ID**4)
    J = np.pi/32*(OD**4 - ID**4)

    properties_dict = {'elastic_modulus': E,
                       'yield_strength': YS,
                       'shear_modulus': G,
                       'poisson_ratio': nu,
                       'x_section_area': A,
                       'moment_inertia_z': Iz,
                       'moment_inertia_y': Iy,
                       'polar_moment_inertia': J,
                       'outer_diameter': OD,
                       'inner_diameter': ID,
                       'density': dens,
                       'cost': cost}

    return properties_dict


def init_file_parser(init_file_path):  # Cristian
    """Parse init file for input parameters.

    Creates ConfigObj object, which reads input parameters as a nested
    dictionary of strings. The string are then converted to their correct types
    using the ConfigObj walk method and a transform function.

    Args:
        init_file_path (string): Path to the init file, relative to
            the directory GASTOp is being executed from.

    Returns:
        config (ConfigObj object): Nested dicitonary of input parameters.

    """
    # Extract inputs from the file as strings, if path exists
    if os.path.isfile(init_file_path):
        config = configobj.ConfigObj(init_file_path)
    else:
        raise IOError("No such path to init file.")

    def transform(section, key):
        """convert each string in config to associated type

        Args:
            section: section of the file
            key: key for dictionary

        Returns:
            Returns each string

        """
        val = section[key]
        newval = val
        # Convert string to float or int
        try:
            newval = float(val)
            newval = int(val)
        except ValueError:
            pass
        # Convert string to True, False, None
        if val == 'True' or val == 'true' or val == 'yes':
            newval = True
        elif val == 'False' or val == 'false' or val == 'no':
            newval = False
        elif val == 'None' or val == 'none':
            newval = None
        # Convert string to numpy array
        try:
            a = ast.literal_eval(val)
            if isinstance(a, list):
                newval = np.array(a)
        except:
            pass
        section[key] = newval

    # Recursively walk through config object converting strings according to
    # transform function.
    config.walk(transform)

    properties_dict = beam_file_parser(config['general']['properties_path'])
    user_spec_nodes = config['general']['user_spec_nodes']
    num_user_nodes = user_spec_nodes.shape[0]
    num_rand_nodes = config['general']['num_rand_nodes']
    num_nodes = num_user_nodes + num_rand_nodes
    num_edges = config['general']['num_rand_edges']
    num_matl = properties_dict['elastic_modulus'].shape[0]
    loads = config['general']['loads']
    fixtures = config['general']['fixtures']

    progress_fitness = config['monitor_params']['progress_fitness']  # sfr
    progress_truss = config['monitor_params']['progress_truss']  # sfr

    if loads.ndim < 3:
        loads = np.reshape(loads, (loads.shape + (1,)))
    if fixtures.ndim < 3:
        fixtures = np.reshape(fixtures, (fixtures.shape + (1,)))
    num_loads = loads.shape[2]
    fixtures = np.concatenate((fixtures, np.zeros(
        (num_rand_nodes, 6, num_loads))), axis=0)
    loads = np.concatenate((loads, np.zeros(
        (num_rand_nodes, 6, num_loads))), axis=0)
    domain = config['general']['domain']

    # ga_params
    config['ga_params']['current_generation'] = 0
    if config['ga_params']['save_filename_prefix']:
        config['ga_params']['config_save_name'] = config['ga_params']['save_filename_prefix'] + '_config.json'
        config['ga_params']['pop_save_name'] = config['ga_params']['save_filename_prefix'] + \
            '_population.json'
    else:
        config['ga_params']['config_save_name'] = 'config.json'
        config['ga_params']['pop_save_name'] = 'population.json'
    if not config['ga_params']['save_frequency']:
        config['ga_params']['save_frequency'] = 0

    # evaluator_params
    config['evaluator_params']['boundary_conditions'] = {}
    config['evaluator_params']['boundary_conditions']['loads'] = loads
    config['evaluator_params']['boundary_conditions']['fixtures'] = fixtures
    config['evaluator_params']['properties_dict'] = properties_dict

    # fitness params
    if config['fitness_params']['parameters']['critical_nodes'] is '':
        config['fitness_params']['parameters']['critical_nodes'] = np.array([])

    # random params
    config['random_params']['num_rand_nodes'] = num_rand_nodes
    config['random_params']['num_rand_edges'] = num_edges
    config['random_params']['domain'] = domain
    config['random_params']['num_material_options'] = num_matl
    config['random_params']['user_spec_nodes'] = user_spec_nodes
    if not config['random_params']['rng_seed']:
        config['random_params']['rng_seed'] = 1729

    # crossover params
    config['crossover_params']['user_spec_nodes'] = user_spec_nodes

    # mutator params
    config['mutator_params']['user_spec_nodes'] = user_spec_nodes
    config['mutator_params']['node_mutator_params']['boundaries'] = domain
    config['mutator_params']['node_mutator_params']['int_flag'] = False
    config['mutator_params']['edge_mutator_params']['boundaries'] = np.array(
        [[-1, -1], [num_nodes, num_nodes]])
    config['mutator_params']['edge_mutator_params']['int_flag'] = True
    config['mutator_params']['property_mutator_params']['boundaries'] = np.array([
                                                                                 [0], [num_matl]])
    config['mutator_params']['property_mutator_params']['int_flag'] = True

    # defaults or user override
    if not config['crossover_params']['node_crossover_method']:
        config['crossover_params']['node_crossover_method'] = 'uniform_crossover'
    if not config['crossover_params']['edge_crossover_method']:
        config['crossover_params']['edge_crossover_method'] = 'uniform_crossover'
    if not config['crossover_params']['property_crossover_method']:
        config['crossover_params']['property_crossover_method'] = 'uniform_crossover'

    if not config['mutator_params']['node_mutator_method']:
        config['mutator_params']['node_mutator_method'] = 'gaussian'
        config['mutator_params']['node_mutator_params']['std'] = .1
    if not config['mutator_params']['edge_mutator_method']:
        config['mutator_params']['edge_mutator_method'] = 'pseudo_bit_flip'
        config['mutator_params']['edge_mutator_params']['proportions'] = 0.3
    if not config['mutator_params']['property_mutator_method']:
        config['mutator_params']['property_mutator_method'] = 'pseudo_bit_flip'
        config['mutator_params']['property_mutator_params']['proportions'] = 0.3

    if not config['selector_params']['method']:
        config['selector_params']['method'] = 'inverse_square_rank_probability'
        config['selector_params']['method_params'] = {}

    if not config['ga_params']['num_elite']:
        config['ga_params']['num_elite'] = int(np.ceil(
            .01*config['ga_params']['pop_size']))
    if not config['ga_params']['percent_crossover']:
        config['ga_params']['percent_crossover'] = 0.4
    if not config['ga_params']['percent_mutation']:
        config['ga_params']['percent_mutation'] = 0.4
    if (config['ga_params']['percent_mutation'] + config['ga_params']['percent_crossover']) > 1:
        raise RuntimeError('percent_crossover + percent_mutation > 1')

    if not config['monitor_params']['progress_fitness']:  # sfr
        config['monitor_params']['progress_fitness'] = False
    if not config['monitor_params']['progress_truss']:  # sfr
        config['monitor_params']['progress_truss'] = False

    return config


def save_progress_history(progress_history, path_progress_history='progress_history.json'):
    '''Saves the population history (progress_history) to a JSON file.

    Args:
        progress_history (dict): History of each generation, including generation
            number, fittest truss, etc.
        path_progress_history (string): Path to save progress_history data file. If file
            doesn't exist, creates it.

    Returns:
        Nothing
    '''
    # Save pop_progress data
    with open(path_progress_history, 'w') as f:
        progress_history_dumped = json.dumps(
            progress_history, cls=encoders.PopulationEncoder)
        json.dump(progress_history_dumped, f)


def load_progress_history(path_progress_history='progress_history.json'):
    '''Loads the population history (progress_history) from a JSON file.

    Args:
        path_progress_history (string): Path to progress_history data file.

    Returns:
        progress_history (dict): History of each generation, including generation
            number, fittest truss, etc.
    '''
    # Load pop_progress data
    with open(path_progress_history, 'r') as f:
        progress_history_loaded = json.load(f)
    progress_history = json.loads(
        progress_history_loaded, object_hook=encoders.numpy_decoder)
    # Bundle truss dictionaries as Truss objects
    for gen in progress_history.keys():
        progress_history[gen]['Best Truss'] = Truss(
            **progress_history[gen]['Best Truss'])

    return progress_history
