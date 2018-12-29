import numpy as np
import configobj
import ast


def beam_file_parser(properties_path):
    """Parses csv file of beam material properties

    Each line of the properties file denotes one type of beam, with a specified
    cross section and material properties.

    Property entries should be formatted as:
    beam #, material name, OD (m), ID (m), elastic_modulus (Pa),
    yield_strength (Pa), density (kg/m^3), poisson_ratio

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
                       'density': dens}

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
    # Extract inputs from the file as strings
    config = configobj.ConfigObj(init_file_path)

    # Function used to convert each string in config to associated type
    def transform(section, key):
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
            if type(a) is list:
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
    if loads.ndim < 3:
        loads = np.reshape(loads, (*loads.shape, 1))
    if fixtures.ndim < 3:
        fixtures = np.reshape(fixtures, (*fixtures.shape, 1))
    num_loads = loads.shape[2]
    fixtures = np.concatenate((fixtures, np.zeros(
        (num_rand_nodes, 6, num_loads))), axis=0)
    loads = np.concatenate((loads, np.zeros(
        (num_rand_nodes, 6, num_loads))), axis=0)
    domain = config['general']['domain']

    # ga_params
    config['ga_params']['current_generation'] = 0

    # evaluator_params
    config['evaluator_params']['boundary_conditions'] = {}
    config['evaluator_params']['boundary_conditions']['loads'] = loads
    config['evaluator_params']['boundary_conditions']['fixtures'] = fixtures
    config['evaluator_params']['properties_dict'] = properties_dict

    # random params
    config['random_params']['num_rand_nodes'] = num_rand_nodes
    config['random_params']['num_rand_edges'] = num_edges
    config['random_params']['domain'] = domain
    config['random_params']['num_material_options'] = num_matl
    config['random_params']['user_spec_nodes'] = user_spec_nodes

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

    if not config['ga_params']['num_elite']:
        config['ga_params']['num_elite'] = int(np.ceil(
            .01*config['ga_params']['pop_size']))
    if not config['ga_params']['percent_crossover']:
        config['ga_params']['percent_crossover'] = 0.4
    if not config['ga_params']['percent_mutation']:
        config['ga_params']['percent_mutation'] = 0.4
    if (config['ga_params']['percent_mutation'] + config['ga_params']['percent_crossover']) > 1:
        raise RuntimeError('percent_crossover + percent_mutation > 1')

    return config


def cart2sph(x, y, z):
    """Converts cartesian coordinates to spherical coordinates

    Args:
        x,y,z (array like): cartesian coordinates. Arrays must all have same shape

    Returns:
        3-element tuple containing:

        - **r** (*ndarray*): Radial coordinate. computed as L2 norm of x,y,z vector.
        - **elev** (*ndarray*):  Elevation angle, in radians. Ranges from pi/2 to
          -pi/2. Elevation = 0 corresponds to a vector in the x-y plane,
          elevation = pi/2 corresponds to a vector along positive z axis.
        - **azim** (*ndarray*): Azimuth angle, in radians. ranges from 0 to 2pi. 
          Azimuth = 0 along the positive x axis.
    """

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    r = np.sqrt(x**2+y**2+z**2)
    azim = np.arctan2(y, x)
    elev = np.pi/2 - np.arccos(z/r)

    return r, elev, azim
