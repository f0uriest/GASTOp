import numpy as np


def beam_file_parser(filename):
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

    OD = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=2)
    ID = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=3)
    E = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=4)
    YS = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=5)
    dens = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=6)
    nu = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=7)
    G = E/(2*(1+nu))
    A = np.pi/4*(OD**2 - ID**2)
    Iz = np.pi/64*(OD**4 - ID**4)
    Iy = np.pi/64*(OD**4 - ID**4)
    J = np.pi/32*(OD**4 - ID**4)

    beam_dict = {'elastic_modulus': E,
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

    return beam_dict


def init_file_parser(init_file_path):
    # Gets all of the inputs from the file
    pass


def cart2sph(x, y, z):
    '''Converts cartesian coordinates to spherical coordinates
    inputs: x,y,z array like
    ouputs r, theta, phi arrays of same length as x,y,z
    angles in radians
    '''
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    r, phi, theta = np.zeros(x.size), np.zeros(x.size), np.zeros(x.size)
    r = np.sqrt(x**2+y**2+z**2)
    phi = np.arctan2(y, x)
    theta = np.arccos(z/r)
    return r, theta, phi
