class boundaries(object):
    # user_spec_nodes: numpy array nx3 [x,y,z] coords of nodes with boundary conditions
    # each user specified node can either have a load, be fixed, or be free with no load
    # loads: numpy array nx6 [Fx,Fy,Fz,Mx,My,Mz]
    # fixed_points: numpy array nx6 [Dx,Dy,Dz,0x,0y,0z] (0 = theta), binary
    #               where O is fixed and 1 is free to displace
    # interferences: numpy array that we can maybe get to later
    #

    def __init__(self,user_spec_nodes,loads,fixtures,interferences = None):
        self._user_spec_nodes = user_spec_nodes #numpy.array
        self._loads = loads #numpy.array
        self._fixed_points = fixtures #numpy.array
        self._interferences = interferences #numpy.array

class fitness_function(object):
    # equation: string flag to denote which hard-coded method to use
    # weights: numpy array

    def __init__(self,equation,weights):
        self._equation = equation
        self._weights = weights

    def sum_of_squares(self,truss):
        # Hard coded equation that takes in
        pass

    def __call__(self,truss):
        pass
