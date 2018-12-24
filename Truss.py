import matplotlib.pyplot as plt


class Truss():
    #
    # nodes: np array num_rand_nodesx3 matrix (xi,yi,zi)
    # edges: np array num_edgesx2 array (starting node #,ending node #)
    # properties: np array num_edgesx1 includes material and cross section
    # fos: np array num_edgesx1
    # deflection: np array num_all_nodesx6 where num_all_nodes = num_rand_nodes+num_user_spec_nodes
    # mass: double
    # cost: double
    # num_joints: int
    # fitness_score: double

    def __init__(self, user_spec_nodes, rand_nodes, edges, properties,
    fos=None,deflection=None,mass=None,cost=None,num_joints=None,fitness_score=None):
        self.user_spec_nodes = user_spec_nodes
        self.rand_nodes = rand_nodes
        self.edges = edges
        self.properties = properties
        self.fos = fos
        self.deflection = deflection
        self.mass = mass
        self.cost = cost
        self.num_joints = num_joints
        self.fitness_score = fitness_score

    def sort(self):
        pass

    def plot(self):
        # plots specific views of the truss object
        pass
