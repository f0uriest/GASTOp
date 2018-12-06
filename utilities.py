class Boundaries():
    # user_spec_nodes: numpy array nx3 [x,y,z] coords of nodes with boundary conditions
    # each user specified node can either have a load, be fixed, or be free with no load
    # loads: numpy array nx6 [Fx,Fy,Fz,Mx,My,Mz]
    # fixed_points: numpy array nx6 [Dx,Dy,Dz,0x,0y,0z] (0 = theta), binary
    #               where O is fixed and 1 is free to displace
    # interferences: numpy array that we can maybe get to later
    #

    def __init__(self,user_spec_nodes,loads,fixtures,interferences = None):
        self.user_spec_nodes = user_spec_nodes #numpy.array
        self.loads = loads #numpy.array
        self.fixed_points = fixtures #numpy.array
        self.interferences = interferences #numpy.array

class FitnessFunction():
    # equation: string flag to denote which hard-coded method to use
    # weights: numpy array

    def __init__(self,equation,weights):
        self.equation = equation
        self.weights = weights

    def sum_of_squares(self,truss):
        # Hard coded equation that takes in
        pass

    def __call__(self,truss):
        pass


def beam_file_parser(matdic_file,dim_file):

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
