import numpy as np
import Truss

class Crossover():

    '''

    Mixes attributes belonging to two different parents to produce two children with
    specific characteristics from both parents.

    When creating a new Crossover() obejct, must be initialized with dictionary
    crossover_params (containing crossover method). Object can then be used as a
    function that produces children according to the specified method.

    Attributes:
        crossover_params(dict of str: ): Dictionary of parameters required by crossover objects.
        crossover_params['method'](str): Name of chosen crossover method.

    '''

    def __init__(self,crossover_params):
        self.params = crossover_params

    def uniform_crossover(self, truss_1, truss_2 ,uniform_crossover_params=None): #Paul
        '''Performs a uniform crossover on the two parents

        The uniform crossover method creates two child arrays by randomly mixing together
        information taken from two parent arrays. To do this, the method creates two arrays
        of ones and zeros -one being the complement of the other- with the same shape as
        the parent arrays. The first array is multiplied with parent1 and the complementary
        array is multiplied with parent2 before adding the results together to make child1.
        The exact opposite multiplication is done to make child2.

        Args:
            truss_1 (array): Numpy array containing information for parent 1
            truss_2 (array): Numpy array containing information for parent 2
            uniform_crossover_params (dictionary): parameters containing any information
                needed for the method.

        Returns:
            child1 (array): Numpy array containing information for child 1
            child2 (array): Numpy array containing information for child 2
        '''
        # find the shape of the parents
        nn = np.shape(truss_1)

        # making an array of ones and zeros
        unos_and_zeros = np.random.randint(2, size=nn)

        # creating an array of all ones to later create the complementary array
        unos = np.ones(nn, dtype=int)

        # creating the complementary array
        unos_and_zeros_c = unos - unos_and_zeros

        # making kids ;)
        child1 = (unos_and_zeros * truss_1) + (unos_and_zeros_c * truss_2)
        child2 = (unos_and_zeros_c * truss_1) + (unos_and_zeros * truss_2)

        # checks for flag that specifies whether output should be an integer and rounds the \
        # output arrays
        if uniform_crossover_params:
            if (uniform_crossover_params['int_flag']==True):
                child1 = (np.rint(child1)).astype(int)
                child2 = (np.rint(child2)).astype(int)

        return child1, child2

    def single_point_split(self, array_1, array_2, single_point_split_params=None): #Amlan

        '''

        Takes specific values of two parents and return two children containing
        characteristics from both parents.

        Chooses a random point and splits the two parents into two different parts.
        Merges the first half of the first parent with the second half of the second
        parent and vice versa.

        Args:
            parents (numpy arrays): the parent arrays.
            single_point_split_params (dictionary): Dictionary containing the domain
            for which the problem is valid

        Returns:
            children (numpy arrays): Numpy arrays containing values from both the parents

        '''

        # Choosing a random point
        array_row = len(array_1)
        point = np.random.randint(0, array_row)

        # Mixing the two parents
        child_1 = np.concatenate((array_1[:point],array_2[point:]),axis=0)
        child_2 = np.concatenate((array_2[:point],array_1[point:]),axis=0)

        # Checking for flag to force integer output
        if single_point_split_params:
            if (single_point_split_params['int_flag']==True):
                child_1 = (np.rint(child_1)).astype(int)
                child_2 = (np.rint(child_2)).astype(int)

        return child_1, child_2

    def two_points_split(self, array_1, array_2, two_points_split_params=None): #Amlan

        '''

        Takes specific values of two parents and return two children containing
        characteristics from both parents.

        Chooses two random points and splits the two parents into three different parts.
        Replaces the central part of the first parent with the central part of the second
        parent.

        Args:
            parents (numpy arrays): the parent arrays.
            two_points_split_params (dictionary): Dictionary containing the domain
            for which the problem is valid

        Returns:
            children (numpy arrays): Numpy arrays containing values from both the parents

        '''
        # Choosing two random points
        p1 = np.random.randint(1,len(array_1))
        p2 = np.random.randint(1,len(array_1)-1)

        # Preparing the two points such that p1<p2
        if p2 >= p1:
            p2 += 1
        else:
            p1, p2 = p2, p1

        # # Mixing the two parents
        child_1 = array_1
        child_2 = array_2
        child_1[p1:p2,:], child_2[p1:p2,:] = child_2[p1:p2,:], child_1[p1:p2,:]

        # Checking for flag to force integer output
        if two_points_split_params:
            if (two_points_split_params['int_flag']==True):
                child_1 = (np.rint(child_1)).astype(int)
                child_2 = (np.rint(child_2)).astype(int)

        return child_1, child_2

    def __call__(self,truss_1,truss_2):

        node_method = getattr(self,self.params['node_crossover_method'])
        edge_method = getattr(self,self.params['edge_crossover_method'])
        property_method = getattr(self,self.params['property_crossover_method'])

        child_1 = Truss.Truss(0,0,0)
        child_2 = Truss.Truss(0,0,0)
        child_1.nodes, child_2.nodes = node_method(truss_1.nodes,truss_2.nodes,self.params['node_crossover_params'])
        child_1.edges, child_2.edges = edge_method(truss_1.edges,truss_2.edges,self.params['edge_crossover_params'])
        child_1.properties, child_2.properties = property_method(truss_1.properties,truss_2.properties,self.params['property_crossover_params'])

        return child_1, child_2
