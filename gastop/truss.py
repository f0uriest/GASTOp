import matplotlib.pyplot as plt


class Truss():
    """Implements the Truss object, which is the fundamental object/data
    type in GASTOp.

    Each truss is defined by a collection of nodes (points in x,y,z space), 
    edges (connections between nodes), and properties (material and geometric
    properties of the connections between nodes).

    A truss can also have assigned attributes such as factor of safety,
    deflections, mass, cost, or fitness score. These attributes are calculated
    based on the nodes, edges, and properties.
    """

    def __init__(self, user_spec_nodes, rand_nodes, edges,
                 properties, fos=None, deflection=None, mass=None,
                 interference=None, cost=None, num_joints=None,
                 fitness_score=None):
        """Creates a Truss object

        Args:
            user_spec_nodes (ndarray): Array of user specified nodes, such as
                where loads are applied or where the structure is supported.
                Array shape should be nx3, where n is the number of specified
                nodes. Each row should contain the x,y,z coordinates of a node.
            rand_nodes (ndarray): Randomly generated nodes. No loads or supports
                should be assigned to random nodes, as their position may change.
                Array shape should be mx3 where m is the number of random
                nodes. Each row should contain the x,y,z coordinates of a node.
            edges (ndarray): Array of connections between nodes. Array shape
                should be kx2, where k is the number of connections or beams
                in the structure. Each row should be 2 integers, the first being
                number of the starting node and the second being the ending node.
                A value of -1 indicates no connection, and will be ignored.
            properties (ndarray): Array of indices for beam properties. Array
                shape should be a 1d array of length k, where k is the number of 
                connections or beams in the structure. Each entry should be an
                integer index into the properties dictionary, with values 
                between [0, number of beam types].
            fos (ndarray): Array of factor of safety values. Default None. 
            deflection (ndarray): Array of node deflections under load,
                in meters. Default None.
            mass (float): Mass of the structure, in kilograms. Default None.
            interference (float): Total length of members passing through
                user specified areas. Default None.
            cost (float): Cost of the structure in dollars. Default None.
            num_joints (int): Number of connections between members. Default None.
            fitness_score (float): Fitness score of the truss. Default None.

        Returns:
            Truss object.
        """
        self.user_spec_nodes = user_spec_nodes
        self.rand_nodes = rand_nodes
        self.edges = edges
        self.properties = properties
        self.fos = fos
        self.deflection = deflection
        self.mass = mass
        self.interference = interference
        self.cost = cost
        self.num_joints = num_joints
        self.fitness_score = fitness_score

    def sort(self):
        """Not implemented yet.

        TODO: method to sort or hash truss object so that two trusses can be
        meaningfully compared.
        """
        pass

    def plot(self):
        """Not implemented yet.

        TODO: method to plot specific views of the truss object.
        See: :meth:`gastop.utilities.truss_plot`
        """
        pass
