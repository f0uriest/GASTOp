class Mutator():
'''
Mutator() object does this...
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
        # makes an array of the same size as the one given with random values\
        # pulled from a normal distribution with mean 0 and std given
        gauss_val = np.random.normal(0, self.gaussian_params['std'], len(array))

        # making a random array of values 0 to 1 which will serve as the random\
        # mutation probability for each value in the array
        rand = np.random.random_sample(size=len(array))

        # creates the new mutated array with values mutated at the indices where\
        #the mutation probability was greater than the randomly generated probability (rand)
        new_array = array + gauss_val*(rand < self.gaussian_params['mutation_probability'])
        
        # clips the numbers that are out of bounds and brings it to the boundary
        new_array = np.clip(new_array, self.gaussian_params['boundaries'])
        
        return new_array

    def pseudo_bit_flip(self,array, bit_flip_params): #Amlan
        '''
        You have a user specified probability that each of the components in the
        truss (nodes, edges, material) will be 'mutated'. Generate a random
        array of numbers which has the same dimensions as the array you are
        working (for example, x, y and z in nodes). If the current number is
        less than user specified probablity for that component, then the number
        gets by a random number in domain specified by the user [xmin, xmax,
        ymin, ymax, zmin, zmax]
        '''
        pass

    def __call__(self,truss):
        node_method = getattr(self,self.params['node_mutator'])
        edge_method = getattr(self,self.params['edge_mutator'])
        property_method = getattr(self,self.params['property_mutator'])
        truss.nodes = node_method(truss.nodes,self.params['nodes'])
        truss.edges = edge_method(truss.edges,self.params['edges'])
        truss.properties = property_method(truss.properties,
                                           self.params['properties'])
        return truss
