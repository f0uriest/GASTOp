import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import Truss
import Mutator
import Crossover
import Selector
##plt.ion() #look into multithreading this
style.use('fivethirtyeight')

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


    def __init__(self,ga_params,mutate_params,random_params,crossover_params,selector_params,
                 evaluator, fitness_function, properties_df):
        # ********
        self.ga_params = ga_params #
        self.mutate_params = mutate_params
        self.random_params = random_params
        self.crossover_params = crossover_params
        self.selector_params = selector_params
        self.population = None
        self.evaluator = evaluator
        self.fitness_function = fitness_function
        # ********

        # progress monitor stuff
        self.pop_progress = [] #initialize as empty array
        #self.progress_display = progress_display #type of progress display
        # [0,1,2] = [no display, terminal display, plot display], change to text later


    def generate_random(self): # Dan
        # Generates new random chromosomes with uniform distribution
        num_rand_nodes = self.random_params['num_rand_nodes']
        num_rand_edges = self.random_params['num_rand_edges']
        num_user_spec_nodes = self.random_params['num_user_spec_nodes']
        domain = self.random_params['domain']
        # First, generate the new nodes:
        new_nodes = np.random.rand(num_rand_nodes,3)

        Ranges = domain[1]-domain[0]
        for j in range(3):
            new_nodes[:,j] = new_nodes[:,j]*Ranges[j] + domain[0][j]*np.ones(num_rand_nodes)
            #np.random.rand(self.random_params['num_rand_nodes'],3)*Ranges[j] + \


        # 2nd, generate the new edges between the nodes:
        new_edges = np.random.randint(num_rand_nodes + num_user_spec_nodes,
                                        size = (num_rand_edges,2))

        for j in range(num_rand_edges):
            if new_edges[j][0] == new_edges[j][1]: # Check that the indexs are not the same:
                new_edges[j][0] = -1
                new_edges[j][1] = -1

        new_properties = np.random.randint(num_rand_nodes + num_user_spec_nodes,
                                        size = (self.random_params['num_material_options'],1))

        return Truss.Truss(new_nodes,new_edges,new_properties)

        """
        # Check to see if any nodes are unused: - Decided to move this to the solver if needed
        check_array = np.zeros(self.num_rand_nodes,dtype=int)
        for j in range(self.num_rand_edges):
            check_array[new_edges[i][0]] = 1
            check_array[new_edges[i][1]] = 1
        for j in range(len(check_array)):
        """

    def initialize_population(self,pop_size):
        self.ga_params['pop_size'] = pop_size
        self.population = [self.generate_random() for i in range(pop_size)]


    def run(self,num_generations,progress_display):
        if progress_display == 2: #check if figure method of progress monitoring is requested
            # initialize plot:
            fig = plt.figure()
            ax1 = fig.add_subplot(1,1,1)
            plt.ylabel('fos')
            plt.xlabel('iteration')
        #

        for current_gen in range(num_generations): # Loop over all generations:
            for current_truss in self.population: # Loop over all trusses -> PARALLELIZE. Later
                #self.evaluator(self.population(current_truss)) # Run evaluator method. Will store results in Truss Object
                self.fitness_function(current_truss) # Assigns numerical score to each truss
            self.progress_monitor(current_gen,progress_display,ax1)
            self.population = self.update_population(self.population) # Determine which members to
        if progress_display == 2:
            plt.show() #sfr, keep plot from closing right after this completes, terminal will hang until this is closed
        return self.population[0], self.pop_progress

    def progress_monitor(self,current_gen,progress_display,ax1): #Susan
        # three options: plot, progress bar ish thing, no output just append
        # calc population diversity and plot stuff or show current results
        fitscore = [i.fitness_score for i in self.population] #extract factor of safety from each truss object in population
        self.pop_progress.append(self.population) #append to history
        if progress_display == 1:
            print(current_gen,min(fitscore))
        elif progress_display == 2:
            #print(current_gen,min(fitscore))
            ax1.scatter(current_gen,min(fitscore),c=[0,0,0]) #plot minimum fitscore for current gen in black
            plt.pause(0.0001) #pause for 0.0001s to allow plot to update, can potentially remove this

        #could make population a numpy structured array
        # fitness = population(:).fos
        #plt.plot(it,fitness)
        #plt.ylabel('convergence')
        #plt.xlabel('iteration')
        #plt.show()

        #pass

    def update_population(self,population): #Cristian
        ''' Creates new population by performing crossover and mutation, as well
        as taking elites and randomly generating trusses.

        First sorts the population by fitness score, from most fit to least fit.
        Creates selector object from population and method. Calls selector to
        get list of parents for crossover and mutation. Performs crossover and
        mutation.

        Args:
            population (list): List of Truss objects that constitutes the
                current generation.

        Returns:
            population (list): List of Truss objects that constitutes the
                current generation.
        '''

        # Store parameters for readability
        pop_size = self.ga_params['pop_size']
        percent_crossover = self.ga_params['percent_crossover']
        percent_mutation = self.ga_params['percent_mutation']
        num_elite = self.ga_params['num_elite']

        # Sort population by fitness score (lowest score = most fit)
        population.sort(key=lambda x: x.fitness_score)

        # Calculate parents needed for crossover, ensure even number
        num_crossover = round(pop_size*percent_crossover)
        if (num_crossover % 2) != 0: # If odd, increment by 1
            num_crossover += 1
        # Calculate parents needed for mutation
        num_mutation = round(pop_size*percent_mutation)
        # Calculate remaining number of trusses in next population
        num_random = pop_size - num_elite - num_crossover - num_mutation
        if num_random < 0: # Raise exception if input params are unreasonable
            raise RuntimeError('Invalid GenAlg parameters.')

        # Instantiate objects
        selector = Selector.Selector(self.selector_params)
        crossover = Crossover.Crossover(self.crossover_params)
        mutator = Mutator.Mutator(self.mutate_params)

        # Select parents as indices in current population
        crossover_parents = selector(num_crossover, population)
        mutation_parents = selector(num_mutation, population)

        # Save most fit trusses as elites
        pop_elite = population[:num_elite]

        # Portion of new population formed by crossover
        pop_crossover = []
        for i in range(0,num_crossover,2):
            parentindex1 = crossover_parents[i]
            parentindex2 = crossover_parents[i+1]
            parent1 = population[parentindex1]
            parent2 = population[parentindex2]
            child1,child2 = crossover(parent1, parent2)
            pop_crossover.extend([child1,child2])

        # Portion of new population formed by mutation
        pop_mutation = []
        for i in range(num_mutation):
            parentindex = mutation_parents[i]
            parent = population[parentindex]
            child = mutator(parent)
            pop_mutation.append(child)

        # Create new random trusses with remaining spots in generation
        pop_random = [self.generate_random() for i in range(num_random)]

        # Append separate lists to form new generation
        population = pop_elite + pop_crossover + pop_mutation + pop_random
        return population
