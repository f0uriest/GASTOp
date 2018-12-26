import numpy as np
import Truss


class Mutator():

    '''

    Randomly mutates the whole/specific attributes belonging to the parents.

    When creating a new Mutator() obejct, must be initialized with dictionary
    mutator_params (containing mutation method). Object can then be used as a
    function that mutates parents according to the specified method.

    Attributes:
        mutator_params(dict of str: ): Dictionary of parameters required by mutator objects.
        mutator_params['method'](str): Name of chosen mutation method.

    '''

    def __init__(self, mutator_params):
        self.params = mutator_params

    def gaussian(self, array, gaussian_params):  # Paul
        '''Performs a gaussian mutation on the given parent array

        The gaussian mutator method creates a child array by mutating the given parent
        array. The mutation is done by adding a random value from the gaussian distribution
        with a user specified standard deviation to each of the elements in the parent
        array. Since values need to be within a specified boundary, any elements that are
        mutated out of bounds on one side are looped inside the other side by the same
        amount, assuming a periodic boundary.

        Args:
            array (array): Numpy array containing the information for the parent array that
                  is being mutated.
            gaussian_params (dictionary): parameters containing information needed for
                  the method.

        Returns:
            new_array (array): Numpy array containing information for the mutated child
        '''
        nn = np.shape(array)
        # makes an array of the same size as the one given with random values\
        # pulled from a normal distribution with mean 0 and std given
        gauss_val = np.random.normal(0, gaussian_params['std'], nn)

        # creates the new mutated array with values mutated at all indices
        new_array = array + gauss_val

        bounds = gaussian_params['boundaries']
        # clips the numbers that are out of bounds and brings it to the boundary
        # for i in range(nn[1]):
        #    new_array[:,i] = np.clip(new_array[:,i], bounds[i,0], bounds[i,1])

        # checks for flag that specifies whether output should be an integer and rounds the \
        # output arrays
        if (gaussian_params['int_flag'] == True):
            new_array = (np.rint(new_array)).astype(int)

        # new method to handle out of bounds problem: loop around on other side
        new_array = bounds[0,:] + ((new_array-bounds[0,:]) % (bounds[1,:]-bounds[0,:]))

        return new_array

    def pseudo_bit_flip(self, parent, bit_flip_params):  # Amlan
        '''

        Mutate specific values of the parent and return the mutant child.

        The pseudo_bit_flip method creates a random binary matrix with a fixed
        ratio of 1s and 0s, as specified by the user. It also creates another
        matrix with elements within the domain specified by the user. It then replaces
        the values from the original matrix with the corresponding value in the
        new matrix only if the corresponding entry in the binary matrix is 1.

        Args:
            parent (numpy array): the parent array.
            bit_flip_params (dictionary): Parameters containing information needed for
            the method.

        Returns:
            child (numpy array): Numpy array containing characteristics mutated
            from the parent.

        '''

        boundaries = bit_flip_params['boundaries']
        proportions = bit_flip_params['proportions']

        # Random binary matrix with a user-specified ratio of 1s and 0s
        B = np.random.choice([0, 1], size=parent.shape, p=[1.-proportions, proportions])

        # Random matrix whose elements are chosen randomly within the domain
        M = np.random.uniform(boundaries[0, :], boundaries[1, :], parent.shape)

        # Mutating the parent
        child = np.multiply(B, M)+np.multiply((np.ones(parent.shape)-B), parent)

        # Checking for flag to force integer output
        if (bit_flip_params['int_flag'] == True):
            child = (np.floor(child)).astype(int)

        return child

    def shuffle_index(self, parent, shuffle_index_params):
        '''

        Mutate the parent by swapping an index with another in the parent array.

        The shuffle_index method creates two random matrices. It then compares
        the individual entries in the two matrices. If the entry in the first
        matrix is greater than the entry in the second matrix, then it replaces the
        corresponding entry in the original matrix with another such element in
        the original matrix.

        Args:
            parent (numpy array): the parent array.
            shuffle_index_params (dictionary): Parameters containing information needed for
            the method.

        Returns:
            child (numpy array):  Numpy array containing characteristics mutated
            from the parent.

        '''

        A = np.random.random(parent.shape)
        B = np.random.random(parent.shape)

        child = np.copy(parent)

        check = B<A

        child[check] = np.random.permutation(child[check])

        return child

    def __call__(self, truss):
        node_method = getattr(self, self.params['node_mutator_method'])
        edge_method = getattr(self, self.params['edge_mutator_method'])
        property_method = getattr(self, self.params['property_mutator_method'])
        user_spec_nodes = self.params['user_spec_nodes']
        child = Truss.Truss(user_spec_nodes, 0, 0, 0)
        child.rand_nodes = node_method(
            truss.rand_nodes, self.params['node_mutator_params'])
        child.edges = edge_method(
            truss.edges, self.params['edge_mutator_params'])
        child.properties = property_method(
            truss.properties, self.params['property_mutator_params'])
        return child
