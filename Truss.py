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

    def __init__(self, nodes, edges, properties):
        self.nodes = nodes
        self.edges = edges
        self.properties = properties
        self.fos = None
        self.deflection = None
        self.mass = None
        self.cost = None
        self.num_joints = None
        self.fitness_score = None

    def sort(self):
        pass

    def plot(self):
        # plots specific views of the truss object
        pass
