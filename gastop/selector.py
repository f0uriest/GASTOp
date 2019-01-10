"""selector.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the Selector class.

"""
import numpy as np


class Selector():  # Cristian
    ''' Selects parents to be used for crossover and mutation.

    When creating a new Selector() obejct, must be initialized with dictionary
    sel_params (containing selection method). Object can then be used as a
    function that selects parents according to the specified method.

   '''

    def __init__(self, sel_params):
        """Creates a Selector object.

        Args:
            sel_params(dict): Dictionary containing:

                - ``'method'`` *(str)*: Name of chosen selection method.
                - ``'method_params'`` *(dict)*: Dictionary of parameters required by chosen method.

        Returns:
            Selector callable object

        """
        self.sel_params = sel_params
        self.method = getattr(self, sel_params['method'])

    @staticmethod
    def inverse_square_rank_probability(num_parents, population):
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
        a = np.array(range(1, pop_size+1))
        pdf = 1/np.sqrt(a)
        cdf = np.cumsum(pdf)
        cdf_upperbound = cdf[-1]

        # Initialize an array of random floats between 1 and the largest entry
        # in the cdf. Find the indices in the cdf array that the random values
        # would fall. For example, if one random value were 1.9, the corresponding
        # index would be 1 since 1.9 lies between 1+1/sqrt(2) and
        # 1+1/sqrt(2)+1/sqrt(3).
        rand_vals = np.random.uniform(0, cdf_upperbound, num_parents)
        parents = np.searchsorted(cdf, rand_vals, side='left')
        parents = parents.astype(int)

        return parents

    @staticmethod
    def tournament(num_parents, population, tourn_size, tourn_prob):
        ''' Selects parents according to tournament method.

        Randomly selects truss indices from population in groups called
        tournaments according to "tourn_size." Each tournament is then sorted
        by index (lower means more fit) in ascending order and a single index
        from each tournament is selected. The selection from each tournament is
        chosen probabilistically, assigning the first, most fit, index with
        probability p = tourn_prob, and then subsequent indices by p*(1-p)^n.
        The winners of each tournament are then returned as the parents array.

        Args:
            num_parents (int): The number of parents to select.
            population (list): List of Truss objects that constitutes the
                current generation.
            tourn_size (int): Number of trusses to include in a given tournament.
                Must be <= 31.
            tourn_prob (float): Probability of selecting first index in each tournament.
                Must be between 0 and 1.

        Returns:
            parents (ndarray): Numpy array of indices in population
                corresponding to selected parents.
        '''

        pop_size = len(population)

        # Build ndarray of randomly selected parent indices. Each row in the
        # array corresponds to a tournament, one tournament for each parent.
        rand_dimen = (num_parents, tourn_size)
        rand_vals = np.random.randint(0, pop_size, rand_dimen)
        rand_vals.sort(axis=1)
        # print(rand_vals,rand_vals.shape,rand_vals.max())

        # Build probability array
        generator = (tourn_prob*(1-tourn_prob)**x for x in range(tourn_size))
        a = np.fromiter(generator, float)
        tourn_distribution = a/np.sum(a)  # normalize probabilities

        # Randomly select indices from each row of rand_vals assigning the
        # corresponding probability in tourn_distribution to each element in
        # the row.
        select_ids = np.random.choice(
            tourn_size, num_parents, p=tourn_distribution)
        # print(select_ids,select_ids.shape,select_ids.max())

        # Build parents array, selecting an element from each row of rand_vals
        parents = np.choose(select_ids, rand_vals.T)

        return parents

    def __call__(self, num_parents, population):
        """Calls selector object on a population to get parent indices.

        Args:
            num_parents (int): Number of parents to select.
            population (list): Population of trusses to select from,
                must be sorted by fitness score in ascending order.

        Returns:
            parents (ndarray): Array of indices of parents in population list.
        """

        parents = self.method(num_parents, population, **
                              self.sel_params['method_params'])
        return parents
