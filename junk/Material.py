class Material(): # TO BE DELETED, ONLY LEFT AS REFERENCE FOR RELEVANT MATERIAL PROPERTIES
"""
Material properties will be stored in a .csv file which is read in and turned
into a dictionary within main.  The options are passed to main via a user input
file.
"""

    def __init__(self,ID,name,elastic_modulus,yield_strength,density,poisson_ratio,shear_modulus):
        self.name = name
        self.elastic_modulus = elastic_modulus
        self.yield_strength = yield_strength
        self.density = density
        self.poisson_ratio = poisson_ratio
        self.shear_modulus = elastic_modulus/(2*(1+poisson_ratio))

class Beam():
    """docstring for beam."""
    def __init__(self, material, shape):
        self.material = material
        self.shape = shape
