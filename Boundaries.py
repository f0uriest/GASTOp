class Boundaries():
    # user_spec_nodes: numpy array nx3 [x,y,z] coords of nodes with boundary conditions
    # each user specified node can either have a load, be fixed, or be free with no load
    # loads: numpy array nx6 [Fx,Fy,Fz,Mx,My,Mz]
    # fixed_points: numpy array nx6 [Dx,Dy,Dz,0x,0y,0z] (0 = theta), binary
    #               where 1 is fixed and 0 is free to displace
    # interferences: numpy array that we can maybe get to later
    #

    def __init__(self,user_spec_nodes,loads,fixtures,interferences = None):
        self.user_spec_nodes = user_spec_nodes #numpy array: num_user_spec_nodesx3 [xi,yi,zi]
        self.loads = loads #numpy.array: num_user_spec_nodesx6 [Fx,Fy,Fz,Mx,My,Mz]
        self.fixed_points = fixtures #numpy.array: num_user_spec_nodesx6 [x,y,z,thetax,thetay,thetaz] flags 1 = fixed, 0 = free
        self.interferences = interferences #numpy.array
