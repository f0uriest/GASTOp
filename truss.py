
class truss(object):
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
        self._nodes = nodes
        self._edges = edges
        self._materials = materials
        self._fos = None
        self._deflection = None
        self._mass = None
        self._cost = None
        self._num_joints = None
        self._fitness_score = None

    def sort(self):
        pass

    def plot(self):
        # plots specific views of the truss object
        pass
