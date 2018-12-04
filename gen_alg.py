class gen_alg(object):
    # Attributes:
    # Envelop Dimensions
    # Parameters needed for the GA

    # Random:
    # num_rand_nodes: int, average num of nodes to randomly generate
    # num_rand_edges: int, average num of edges to randomly generate
    # domain: tuple of tuples, envelope dimensions (xmin,xmax;ymin,ymax;zmin,zmax)

    # Crossover
    # crossover_fraction: float (0->1), what ratio of each parent should be taken
    # split_method: flag that says which parent to prefer. TO BE DETERMINED LATER

    # Mutation:
    # stat_var_nodes: double, statistical variance on number of nodes that should be generated
    # stat_var_edges: float (0->1), chance that a new node is assigned to one end
    # stat_var_matl: float (0->1) chance that a new material is assigned


    def __init__(self,\ #check this
    num_rand_nodes,num_rand_edges,domain,\
    crossover_fraction = 0.5, split_method = None,\
    stat_var_nodes,stat_var_edges,stat_var_matl):
        #Random
        self._num_rand_nodes = num_rand_nodes
        self._num_rand_edges = num_rand_edges
        self._domain = domain
        # Crossover
        self._crossover_fraction = crossover_fraction
        self._split_method = split_method
        #Mutation
        self._stat_var_nodes = stat_var_nodes
        self._stat_var_edges = stat_var_edges
        self._stat_var_matl = stat_var_matl

    def generate_random(self):
        # Generates new random chromosomes with uniform distribution
        pass

    def crossover(self,truss_1,truss_2):
        #
        pass

    def mutation(self,truss):
        #
        pass

    def selector(self,population):
        #
        pass

    def progress_monitor(self,population):
        # calc population diversity and plot stuff or show current results
        pass
