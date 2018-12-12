import numpy as np

class Mutator():
# Mutator() object does this...


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
        gauss_val = np.random.normal(0, self.gaussian_params['std'], nn)
        
        # creates the new mutated array with values mutated at all indices
        new_array = array + gauss_val

        bounds = self.gaussian_params['boundaries']
        # clips the numbers that are out of bounds and brings it to the boundary
        for i in range(nn[1]):
            new_array[:,i] = np.clip(new_array[:,i], bounds[i,0], bounds[i,1])
        
        return new_array

    def pseudo_bit_flip(self,array, bit_flip_params): #Amlan
        '''
        You have a user specified probability that each of the components in the
        truss (nodes, edges, material) will be 'mutated'. Generate a random
        array of numbers which has the same dimensions as the array you are
        working with (for example, x, y and z in nodes). If the current number is
        less than user specified probablity for that component, then the number
        gets flipped by a random number in the user specified domain [for
        example: xmin, xmax, ymin, ymax, zmin, zmax]
        '''
        (array_row,array_col) = array.shape
        # bit_flip_params may be a dictionary, in which case, you need to change the following
        # For now, assume it's an numpy array.
        # e.g. [[xmin, ymin, zmin],[xmax,ymax,zmax]]
        bounds = bit_flip_params['bounds']

        prob_mat = np.zeros(array.shape)

        for j in range(array_col):
            lower_bound, upper_bound = bounds[0,j], bounds[1,j]
            prob_mat[:,j] = np.random.uniform(lower_bound,upper_bound,len(array[:,j]))
            for i in range(array_row):
                if prob_mat[i,j]>array[i,j]:
                    array[i,j] = np.random.uniform(lower_bound,upper_bound)

        return array

    def __call__(self,truss):
        node_method = getattr(self,self.params['node_mutator'])
        edge_method = getattr(self,self.params['edge_mutator'])
        property_method = getattr(self,self.params['property_mutator'])
        truss.nodes = node_method(truss.nodes,self.params['nodes'])
        truss.edges = edge_method(truss.edges,self.params['edges'])
        truss.properties = property_method(truss.properties,
                                           self.params['properties'])
        return truss
