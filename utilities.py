import numpy as np


def beam_file_parser(matdic_file, dim_file):
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
    pass


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
