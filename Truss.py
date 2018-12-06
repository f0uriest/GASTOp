
class Truss():
    #
    # nodes: np array nx3 matrix (xi,yi,zi)
    # edges: np array mx2 array (starting node #,ending node #)
    # material: np array
    # fos: double
    # deflection: np array
    # mass: double
    # cost: double
    # num_joints: int
    # fitness_score: double

    def __init__(self, nodes, edges, materials):
        self.nodes = nodes
        self.edges = edges
        self.materials = materials
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
