import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import configobj
import ast


def beam_file_parser(properties_path):
    """
    Inputs:
    - Init file material path
    - Init file shape,mat,etc

    For each item in the list:
    Grab the appropriate material info for that member
    material(self,name,elastic_modulus,yield_strength,density,poisson_ratio,shear_modulus)


   Possible Material Properties .csv file (nominally not touched by user)s:
   Full Name, abreviated_name, E, v, yield strength

   User input file format:

   Possible Members:
   mat option 1 , c/s 1, inner dim 1, outer dim 1
   mat option 2 , c/s 2, inner dim 2, outer dim 2
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
    ''' Parse init file for input parameters.

    Creates ConfigObj object, which reads input parameters as a nested
    dictionary of strings. The string are then converted to their correct types
    using the ConfigObj walk method and a transform function.

    Args:
        init_file_path (string): Path to the init file.

    Returns:
        config (ConfigObj object): Nested dicitonary of input parameters as
            correct types.
    '''
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
        if val == 'True':
            newval = True
        elif val == 'False':
            newval = False
        elif val == 'None':
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

    return config


def cart2sph(x, y, z):
    """Converts cartesian coordinates to spherical coordinates

    Args:
        x,y,z (array like): cartesian coordinates. Arrays must all have same shape

    Returns:
        r (ndarray): radial coordinate, L2 norm of x,y,z vector.
        theta (ndarray): elevation angle, in radians. Ranges from pi/2 to -pi/2
            theta = 0 corresponds to a vector in the x-y plane, theta = pi/2
            along positive z axis.
        phi (ndarray): azimuthal angle, in radians. Ranges from 0 to 2pi.
            phi = 0 along positive x axis.
    """

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    r = np.sqrt(x**2+y**2+z**2)
    phi = np.arctan2(y, x)
    theta = np.pi/2 - np.arccos(z/r)

    return r, theta, phi


def truss_plot(truss, domain=None, loads=None, fixtures=None):
    """Plots a truss object as a 3D wireframe

    Args:
        truss (Truss object): truss to be plotted. Must have user_spec_nodes,
            rand_nodes, edges defined.
        domain (ndarray): (optional) axis limits in x,y,z, specified as a
            3x2 array: [[xmin, xmax],[ymin,ymax],[zmin,zmax]].
        loads (ndarray): (optional) Array of loads to be plotted as arrows.
            Specified as nx6 array, each row corresponding to the load at 
            the node matching the row #. Load format:
            [Fx,Fy,Fz,Mx,My,Mz]
        fixtures (ndarray): (optional) Array of fixtures to be plotted as blobs.
            Specified as an nx6 array, each row corresponding to fixtures at
            the node matching the row #. Format:
            [Dx,Dy,Dz,Rx,Ry,Rz] value of 1 means fixed in that direction, 
            value of zero is free.

    Returns:
        None
    """
    nodes = np.concatenate(
        (truss.user_spec_nodes.copy(), truss.rand_nodes.copy()))
    # mark self connected nodes
    truss.edges[truss.edges[:, 0] == truss.edges[:, 1]] = -1
    con = truss.edges.copy()
    matl = truss.properties.copy()

    # remove self connected edges
    matl = matl[(con[:, 0]) >= 0]
    matl = matl[(con[:, 1]) >= 0]
    con = con[(con[:, 0]) >= 0]
    con = con[(con[:, 1]) >= 0]

    num_nodes = nodes.shape[0]
    num_con = con.shape[0]

    # need to add stuff for plotting loads/fixtures

    edge_vec_start = nodes[con[:, 0], :]
    edge_vec_end = nodes[con[:, 1], :]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    if domain is not None:
        ax.set_xlim(domain[0, :])
        ax.set_ylim(domain[1, :])
        ax.set_zlim(domain[2, :])
    for i in range(num_con):
        ax.plot([edge_vec_start[i, 0], edge_vec_end[i, 0]],
                [edge_vec_start[i, 1], edge_vec_end[i, 1]],
                [edge_vec_start[i, 2], edge_vec_end[i, 2]])

    plt.show()
