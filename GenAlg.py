import matplotlib.pyplot as plt
import numpy as np
import Truss
import Mutator
import Crossover
import Selector

class GenAlg():
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
    # stat_stdev_nodes: double, statistical standard deviation on number of nodes that should be generated
    # stat_stdev_edges: float (0->1), chance that a new node is assigned to one end
    # stat_stdev_matl: float (0->1) chance that a new material is assigned


    def __init__(self,ga_params,mutate_params,crossover_params,selector_params,
                 evaluator, fitness_function, properties_df):
        # ********
        self.ga_params = ga_params
        self.mutate_params = mutate_params
        self.crossover_params = crossover_params
        self.selector_params = selector_params
        self.population = None
        self.evaluator = evaluator
        self.fitness_function = fitness_function
        # ********

        self.pop_size = None
        self.num_elite = num_elite #int, ~10 (the whole truss that get passed)
        self.percent_crossover= percent_crossover # double between 0 and 1
        self.percent_mutation = percent_mutation # double between 0 and 1
        #Random
        self.num_rand_nodes = num_rand_nodes # int
        self.num_rand_edges = num_rand_edges # int
        self.domain = domain # np array 2x3 [[xmin,ymin,zmin],[xmax,ymax,zmax]]
        self.boundaries = boundaries


        # Crossover - different crossovers for edges, nodes, properties
        # *** Will end up in the crossover_params ***
        Edge_crossover_fraction = edge_crossover_fraction # double between 0 and 1
        Edge_split_method = edge_split_method # string
        Node_crossover_fraction = node_crossover_fraction
        Node_split_method = node_split_method
        Materials_crossover_fraction = materials_crossover_fraction
        Materials_split_method = materials_split_method

        #Mutation
        self.stat_stdev_nodes = stat_stdev_nodes # double
        self.stat_stdev_edges = stat_stdev_edges # double
        self.stat_stdev_matl = stat_stdev_matl # double
        self.pseudo_bit_flip_prob_nodes = pseudo_bit_flip_prob_nodes # double between 0 and 1
        self.pseudo_bit_flip_prob_edges = pseudo_bit_flip_prob_edges # double between 0 and 1
        self.pseudo_bit_flip_prob_matl = pseudo_bit_flip_prob_matl # double between 0 and 1

        # progress monitor stuff
        self.pop_progress = None

    def generate_random(self): # Dan
        # Generates new random chromosomes with uniform distribution

        # First, generate the new nodes:
        new_nodes = np.ones([self.num_rand_nodes,3])

        Ranges = self.domain[1]-self.domain[0]
        for j in range(3):
            new_nodes[:,j] = np.random.rand(self.num_rand_nodes,j)*Ranges[j]


        # 2nd, generate the new edges between the nodes:
        new_edges = np.random.randint(self.num_rand_nodes + self.boundaries.user_spec_nodes.shape[0],
                                        size = (self.num_rand_edges,2))

        for j in range(self.num_rand_edges):
            if new_edges[j][0] == new_edges[j][1]: # Check that the indexs are not the same:
                new_edges[j][0] = np.nan
                new_edges[j][1] = np.nan


        """
        # Check to see if any nodes are unused: - Decided to move this to the solver if needed
        check_array = np.zeros(self.num_rand_nodes,dtype=int)
        for j in range(self.num_rand_edges):
            check_array[new_edges[i][0]] = 1
            check_array[new_edges[i][1]] = 1
        for j in range(len(check_array)):
        """
    def initialize_population(self,pop_size):
        self.population = [self.generate_random for i in range(pop_size)]
        self.pop_size = pop_size

    def run(num_generations):
        for current_gen in range(num_generations): # Loop over all generations:
            self.progress_monitor(self.population,current_gen)
            for current_truss in range(self.pop_size): # Loop over all trusses -> PARALLELIZE. Later
                self.evaluator(self.population[current_truss]) # Run evaluator method. Will store results in Truss Object
                self.fitness_function(self.population[current_truss]) # Assigns numerical score to each truss
            self.population = self.update_population(self.population) # Determine which members to
        return self.population[0], self.pop_progress

    def progress_monitor(self,population,current_gen): #Susan
        # calc population diversity and plot stuff or show current results
        #self.pop_progress[current_gen] = population
        #plt.plot(it,div)
        #plt.ylabel('convergence')
        #plt.xlabel('iteration')
        #plt.show()

        pass

    def update_population(self,population): #Cristian
        '''
        First do elitism
        create selector object from population and method
        call selector to get list of parents parent selection
        for loop for crossover
        for loop for mutation
        return population
        '''

        # Calls the selector, mutation, crosssover, etc.
        pass
