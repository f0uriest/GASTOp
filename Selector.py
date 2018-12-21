import numpy as np

class Selector(): # Cristian
    ''' Selects parents to be used for crossover and mutation.

    When creating a new Selector() obejct, must be initialized with dictionary
    sel_params (containing selection method). Object can then be used as a
    function that selects parents according to the specified method.

    Attributes:
        sel_params(dict of str: ): Dictionary of parameters required by selector
                                    objects.
        sel_params['method'](str): Name of chosen selection methodself.
        sel_params['tourn_size'](int): Number of indices in each tournament.
                                    Only needed for tournament method.
        sel_params['tourn_prob'](int): Probability of selecting first inde in
                                    each tournament. Only needed for tournament
                                    method.
    '''
    def __init__(self,sel_params):
        self.sel_params = sel_params

    def inverse_square_rank_probability(self,num_parents,population):
        ''' Selects parents according to inverse square rank method.

        Creates a cdf, with each entry the cumulative sum of 1/sqrt(N)
        for N = 1, ... Random values are then produced between the largest and
        smallest elements of the list. Each parent is chosen as the index in the
        cdf that the corresponding random value falls. In this way, the most
        probable parents are those with the highest fitness scores.

        Args:
            num_parents (int): The number of parents to select.
            population (list): List of Truss objects that constitutes the
                current generation.

        Returns:
            parents (ndarray): Numpy array of indices in population
                corresponding to selected parents.
        '''

        pop_size = len(population)

        # Build cdf (cumulative distribution function)
        a = np.array(range(1,pop_size+1))
        pdf = 1/np.sqrt(a)
        cdf = np.cumsum(pdf)
        cdf_upperbound = cdf[-1]

        # Initialize an array of random floats between 1 and the largest entry
        # in the cdf. Find the indices in the cdf array that the random values
        # would fall. For example, if one random value were 1.9, the corresponding
        # index would be 1 since 1.9 lies between 1+1/sqrt(2) and
        # 1+1/sqrt(2)+1/sqrt(3).
        rand_vals = np.random.uniform(0,cdf_upperbound,num_parents)
        parents = np.searchsorted(cdf,rand_vals,side='left')
        parents = parents.astype(int)

        return parents

    def tournament(self,num_parents,population):
        ''' Selects parents according to tournament method.

        (ASSUMES POPULATION IS SORTED BY FITNESS) Randomly selects truss
        indices from population in groups called tournaments according to
        "tourn_size." Each tournament is then sorted by index (lower means
        more fit) in ascending order and a single index from each tournament
        is selected. The selection from each tournament is chosen
        probabilistically, assigning the first, most fit, index with probability
        p = tourn_prob, and then subsequent indices by p*(1-p)^n. The winners
        of each tournament are then returned as the parents array.

        Args:
            num_parents (int): The number of parents to select.
            population (list): List of Truss objects that constitutes the
                current generation.

        Returns:
            parents (ndarray): Numpy array of indices in population
                corresponding to selected parents.
        '''

        tourn_size = self.sel_params['tourn_size']
        tourn_prob = self.sel_params['tourn_prob']
        pop_size = len(population)

        # Build ndarray of randomly selected parent indices. Each row in the
        # array corresponds to a tournament, one tournament for each parent.
        rand_dimen = (num_parents,tourn_size)
        rand_vals = np.random.randint(0,pop_size,rand_dimen)
        rand_vals.sort(axis=1)

        # Build probability array
        generator = (tourn_prob*(1-tourn_prob)**x for x in range(tourn_size))
        a = np.fromiter(generator,float)
        tourn_distribution = a/np.sum(a) # normalize probabilities

        # Randomly select indices from each row of rand_vals assigning the
        # corresponding probability in tourn_distribution to each element in
        # the row.
        select_ids = np.random.choice(tourn_size,pop_size,p=tourn_distribution)

        # Build parents array, selecting an element from each row of rand_vals
        parents = np.choose(select_ids,rand_vals.T)

        return parents

    def __call__(self,num_parents,population):
        method = getattr(self,self.sel_params['method'])
        parents = method(num_parents,population)
        return parents
