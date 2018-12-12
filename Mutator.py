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

        pass

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
        bounds = bit_flip_params

        prob_mat = np.zeros(array.shape)
        
        for col in range(array_col):
            lower_bound, upper_bound = array[:,col].min(), array[:,col].max()
            prob_mat[:,col] = np.random.uniform(lower_bound,upper_bound,len(array[:,col]))

        for j in range(array_col):
            lower_bound = bounds[0,j]
            upper_bound = bounds[1,j]
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
