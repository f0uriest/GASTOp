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


    def __init__(self,mutator_params):
        self.params = mutator_params

    def gaussian(self,array,gaussian_params): #Paul
        '''
        Given an array of data, adding a gaussian number (normal distribution,
        bell curve) with mean 0 and some standard deviation to each number
        in the array. If it is mutated to outside the boundary, move it
        back to the boundary. (use variables specified above) Round the number
        to the nearest integer
        '''
        nn = np.shape(array)
        # makes an array of the same size as the one given with random values\
        # pulled from a normal distribution with mean 0 and std given
        gauss_val = np.random.normal(0, gaussian_params['std'], nn)

        # creates the new mutated array with values mutated at all indices
        new_array = array + gauss_val

        bounds = gaussian_params['boundaries']
        # clips the numbers that are out of bounds and brings it to the boundary
        #for i in range(nn[1]):
        #    new_array[:,i] = np.clip(new_array[:,i], bounds[i,0], bounds[i,1])

        # checks for flag that specifies whether output should be an integer and rounds the \
        # output arrays
        if (gaussian_params['int_flag']==True):
            new_array = (np.rint(new_array)).astype(int)

        # new method to handle out of bounds problem: loop around on other side
        for j in range(nn[1]):
            for i in range(nn[0]):
                if (new_array[i,j] < bounds[j,0]):
                    new_array[i,j] = bounds[j,1] - (new_array[i,j] % bounds[j,0])
                elif (new_array[i,j] > bounds[j,1]):
                    new_array[i,j] = bounds[j,0] + (new_array[i,j] % bounds[j,1])

        return new_array

    def pseudo_bit_flip(self,array, bit_flip_params): #Amlan

        '''

        Mutate specific values of the parent and return the mutant child.

        Creates a random binary matrix with a fixed ratio of 1s and 0s, as specified
        by the user. Creates another matrix with elements within the domain specified
        by the user. Replaces the values from the original matrix with the corresponding
        value in the new matrix only if the corresponding entry in the binary matrix is 1.

        Args:
            parent (numpy array): the parent array.
            bit_flip_params (dictionary): Dictionary containing the domain for which
            the problem is valid, and the proportions of 1s to 0s for the binary matrix.

        Returns:
            child (numpy array): Numpy array containing values mutated from the parent.

        '''

        boundaries = bit_flip_params['boundaries']
        proportions = bit_flip_params['proportions']

        # Random binary matrix with a user-specified ratio of 1s and 0s
        B = np.random.choice([0, 1], size=array.shape, p=[1.-proportions, proportions])

        # Random matrix whose elements are chosen randomly within the domain
        M = np.random.uniform(boundaries[0,:],boundaries[1,:],array.shape)

        # Mutating the parent
        array = np.multiply(B,M)+np.multiply((np.ones(array.shape)-B),array)

        # Checking for flag to force integer output
        if (bit_flip_params['int_flag']==True):
            array = (np.rint(array)).astype(int)

        return array

    def __call__(self,truss):
        node_method = getattr(self,self.params['node_mutator_method'])
        edge_method = getattr(self,self.params['edge_mutator_method'])
        property_method = getattr(self,self.params['property_mutator_method'])
        child = Truss.Truss(0,0,0)
        child.nodes = node_method(truss.nodes,self.params['node_mutator_params'])
        child.edges = edge_method(truss.edges,self.params['edge_mutator_params'])
        child.properties = property_method(truss.properties, self.params['property_mutator_params'])
        return child
