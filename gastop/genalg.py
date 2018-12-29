import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import json
from tqdm import tqdm  # susan added
from multiprocessing import Pool
import os


from gastop import Truss, Mutator, Crossover, Selector, Evaluator, FitnessFunction, encoders, utilities
# plt.ion() #look into multithreading this
style.use('fivethirtyeight')


class GenAlg():
    """Creates, updates, tracks, loads, and saves populations.

    The GenAlg Class orchestrates all of the other functions that perform
    functions to change the population and its elements. In this case, such
    classes are crossover, evaluator, encoders, fitness, mutator, selector, and
    truss.

    In brief, GenAlg calls many other functions in order to create a generation
    which is then analyzed to fully determine its relavant properties. These
    properties are then used to create a new generation and the process repeats
    until a final solution is reached.

    """

    def __init__(self, config):
        """Creates a GenAlg object

        Once created, the object will store all of the relavant information
        about a population. The object also contains the necessary functions to
        modify itself, evaluate its 'goodness', and then create new members for
        the next generation.

        Args:
            Either:
            config (dict): Configuration dictionary with parameters, such as one
                created by :meth:`gastop.utilities.init_file_parser`
            config (str): File path to config file to be parsed. Used
                instead of passing config dictionary directly. 

        Returns:
            GenAlg callable object
        """
        if type(config) is type('str'):
            config = utilities.init_file_parser(config)

        self.config = config
        self.ga_params = config['ga_params']
        self.mutator_params = config['mutator_params']
        self.random_params = config['random_params']
        self.crossover_params = config['crossover_params']
        self.selector_params = config['selector_params']
        self.population = []
        self.evaluator = Evaluator(**config['evaluator_params'])
        self.fitness_function = FitnessFunction(**config['fitness_params'])

        # progress monitor stuff
        self.pop_progress = []  # initialize as empty array
        # self.progress_display = progress_display #type of progress display
        # [0,1,2] = [no display, terminal display, plot display], change to text later
        np.random.seed(0)

    def generate_random(self, _):  # Dan
        '''Generates and returns new truss objects with random properties

        The random method first determines the desired ranges of all values
        that will be calculated. Then, random numbers for the node locations,
        connections, and properties are all determined with the numpy.random
        methods.

        Args:
            self (GenAlg object): Contains the information needed to determine
            the ranges

        Returns:
            (Truss object): Truss object with the newly determined values
        '''
        # Generates new random chromosomes with uniform distribution
        num_rand_nodes = self.random_params['num_rand_nodes']
        num_rand_edges = self.random_params['num_rand_edges']
        user_spec_nodes = self.random_params['user_spec_nodes']
        num_user_spec_nodes = user_spec_nodes.shape[0]
        domain = self.random_params['domain']
        # First, generate the new nodes:
        # Try 1: Time: 0.579
        # Ranges = domain[1]-domain[0]
        # new_nodes = np.random.rand(num_rand_nodes, 3)
        #
        # for j in range(3):
        #     new_nodes[:, j] = new_nodes[:, j]*Ranges[j] + \
        #         domain[0][j]*np.ones(num_rand_nodes)

        # Try 2: Time: 0.499
        # nn1 = np.random.rand(num_rand_nodes, 1)*Ranges[0] + domain[0][0]
        # nn2 = np.random.rand(num_rand_nodes, 1)*Ranges[1] + domain[0][1]
        # nn3 = np.random.rand(num_rand_nodes, 1)*Ranges[2] + domain[0][2]
        # new_nodes = np.concatenate((nn1,nn2,nn3),axis=1)

        # Try 3: Time: 0.451
        # new_nodes = np.empty([num_rand_nodes,3])
        # for j in range(3):
        #     new_nodes[:,j] = np.random.rand(num_rand_nodes)*Ranges[j] + domain[0][j]

        # Try 4: Time: 0.433!
        new_nodes = np.random.uniform(
            domain[0], domain[1], (num_rand_nodes, 3))

        # 2nd, generate the new edges between the nodes:
        new_edges = np.random.randint(num_rand_nodes + num_user_spec_nodes,
                                      size=(num_rand_edges, 2))

        new_properties = np.random.randint(self.random_params['num_material_options'],
                                           size=(num_rand_edges))

        return Truss(user_spec_nodes, new_nodes, new_edges, new_properties)

    def initialize_population(self, pop_size):
        '''Initializes population with randomly creates Truss objects

        Args:
            self (GenAlg object): Object that will be updates

        Returns:
            Updated self.population
        '''
        self.ga_params['pop_size'] = pop_size

        # Try 1: t= 0.298
        # self.population = [self.generate_random() for i in range(pop_size)]

        # Try 2: t= 0.352
        # pool = Pool()
        # result_list = [pool.map_async(self.generate_random, ()) for i in range(pop_size)]
        #
        # self.population = [res.get() for res in result_list]

        # Try 3: t=0.343
        # pool = Pool()
        # pool.map_async(self.generate_random, range(pop_size),callback=self.population.extend)
        # pool.close()
        # pool.join()

        # Try 4: t=0.232
        pool = Pool()
        self.population = pool.map(self.generate_random, range(pop_size))
        pool.close()
        pool.join()

    def run(self, num_generations=None, progress_display=1, num_threads=None):
        if num_threads is None:
            if self.ga_params['num_threads'] is None:
                num_threads = 1
            else:
                num_threads = self.ga_params['num_threads']
        if num_generations is None:
            num_generations = self.ga_params['num_generations']
        else:
            self.ga_params['num_generations'] = num_generations

        if progress_display == 2:  # check if figure method of progress monitoring is requested
            # initialize plot:
            fig = plt.figure()
            ax1 = fig.add_subplot(1, 1, 1)
            plt.ylabel('fos')
            plt.xlabel('iteration')
        #

        # Loop over all generations:

        # Without any parallelization:
        # Try 1: time =
        # for current_gen in tqdm(range(num_generations)):
        #     for current_truss in self.population:  # Loop over all trusses -> PARALLELIZE. Later
        #         # Run evaluator method. Will store refitness_scoresults in Truss Object
        #         self.evaluator(current_truss)
        #         # Assigns numerical score to each truss
        #         self.fitness_function(current_truss)
        #         # print(current_truss.fos)

        #     if progress_display == 2:
        #         self.progress_monitor(current_gen, progress_display, ax1)
        #     self.update_population()  # Determine which members to
        # if progress_display == 2:
        #     plt.show()  # sfr, keep plot from closing right after this completes, terminal will hang until this is closed
        # return self.population[0], self.pop_progress

        # With parallelization
        # Try 2: time =
        for current_gen in tqdm(range(num_generations)):
            self.ga_params['current_generation'] = current_gen
            pool = Pool(num_threads)
            self.population = pool.map(self.evaluator, self.population)
            self.population = pool.map(self.fitness_function, self.population)
            pool.close()
            pool.join()
            if progress_display == 2:
                self.progress_monitor(current_gen, progress_display, ax1)
            self.update_population()  # Determine which members to
        if progress_display == 2:
            plt.show()  # sfr, keep plot from closing right after this completes, terminal will hang until this is closed
        return self.population[0], self.pop_progress

    def progress_monitor(self, current_gen, progress_display, ax1):  # Susan
        # three options: plot, progress bar ish thing, no output just append
        # calc population diversity and plot stuff or show current results
        # extract factor of safety from each truss object in population
        fitscore = [i.fitness_score for i in self.population]
        self.pop_progress.append(self.population)  # append to history
        if progress_display == 1:
            print(current_gen, np.amin(fitscore))
        elif progress_display == 2:
            # print(current_gen,min(fitscore))
            # plot minimum fitscore for current gen in black
            ax1.scatter(current_gen, np.amin(fitscore), c=[0, 0, 0])
            # pause for 0.0001s to allow plot to update, can potentially remove this
            plt.pause(0.0001)

        # could make population a numpy structured array
        # fitness = population(:).fos
        # plt.plot(it,fitness)
        # plt.ylabel('convergence')
        # plt.xlabel('iteration')
        # plt.show()

        # pass

    def save_state(self, dest_config='config.json',
                   dest_pop='population.json'):  # Cristian
        # Save rng_seed for reloading
        self.config['random_params']['rng_seed'] = np.random.get_state()

        config = self.config
        population = self.population

        # Save config data
        with open(dest_config, 'w') as f:
            config_dumped = json.dumps(config, cls=encoders.ConfigEncoder)
            json.dump(config_dumped, f)

        # Save population data
        with open(dest_pop, 'w') as f:
            pop_dumped = json.dumps(population, cls=encoders.PopulationEncoder)
            json.dump(pop_dumped, f)

    def load_state(self, dest_config='config.json',
                   dest_pop='population.json'):  # Cristian
        # Load config data
        with open(dest_config, 'r') as f:
            config_loaded = json.load(f)
        config = json.loads(config_loaded, object_hook=encoders.numpy_decoder)

        # Load population data
        with open(dest_pop, 'r') as f:
            pop_loaded = json.load(f)
        population = json.loads(pop_loaded, object_hook=encoders.numpy_decoder)
        population = (Truss(**dct) for dct in population)

        return config, population

    def update_population(self):  # Cristian
        ''' Creates new population by performing crossover and mutation, as well
        as taking elites and randomly generating trusses.

        First sorts the population by fitness score, from most fit to least fit.
        Creates selector object from population and method. Calls selector to
        get list of parents for crossover and mutation. Performs crossover and
        mutation.
        '''

        # Store parameters for readability
        population = self.population
        pop_size = self.ga_params['pop_size']
        percent_crossover = self.ga_params['percent_crossover']
        percent_mutation = self.ga_params['percent_mutation']
        num_elite = self.ga_params['num_elite']

        # Sort population by fitness score (lowest score = most fit)
        population.sort(key=lambda x: x.fitness_score)

        # Calculate parents needed for crossover, ensure even number
        num_crossover = round((pop_size-num_elite)*percent_crossover)
        if (num_crossover % 2) != 0:  # If odd, decrement by 1
            num_crossover -= 1
            if num_crossover < 0:  # if that makes it negative, make 0
                num_crossover = 0
        # Calculate parents needed for mutation
        num_mutation = round((pop_size-num_elite)*percent_mutation)
        # Calculate remaining number of trusses in next population
        num_random = pop_size - num_elite - num_crossover - num_mutation
        if num_random < 0:  # Raise exception if input params are unreasonable
            raise RuntimeError('Invalid GenAlg parameters.')

        # Instantiate objects
        selector = Selector(self.selector_params)
        crossover = Crossover(self.crossover_params)
        mutator = Mutator(self.mutator_params)

        # Select parents as indices in current population
        crossover_parents = selector(num_crossover, population)
        mutation_parents = selector(num_mutation, population)

        # Save most fit trusses as elites
        pop_elite = population[:num_elite]

        # Portion of new population formed by crossover
        pop_crossover = []
        for i in range(0, num_crossover, 2):
            parentindex1 = crossover_parents[i]
            parentindex2 = crossover_parents[i+1]
            parent1 = population[parentindex1]
            parent2 = population[parentindex2]
            child1, child2 = crossover(parent1, parent2)
            pop_crossover.extend((child1, child2))

        # Portion of new population formed by mutation
        pop_mutation = []
        for i in range(num_mutation):
            parentindex = mutation_parents[i]
            parent = population[parentindex]
            child = mutator(parent)
            pop_mutation.append(child)

        # Create new random trusses with remaining spots in generation
        pop_random = [self.generate_random(2) for i in range(num_random)]

        # Append separate lists to form new generation
        population = pop_elite + pop_crossover + pop_mutation + pop_random

        # Update population attribute
        self.population = population
