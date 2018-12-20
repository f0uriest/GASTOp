import numpy as np

class Selector(): # Cristian
    ''' Selects parents to be used for crossover and mutation.

    When creating a new Selector() obejct, must be initialized with dictionary
    sel_params (containing selection method). Object can then be used as a
    function that selects parents according to the specified method.
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

        Explain...

        Args:
            num_parents (int): The number of parents to select.
            population (list): List of Truss objects that constitutes the
                current generation.

        Returns:
            parents (ndarray): Numpy array of indices in population
                corresponding to selected parents.
        '''
        

        pass

    def __call__(self,num_parents,population):
        method = getattr(self,self.sel_params['method'])
        parents = method(num_parents,population)
        return parents
