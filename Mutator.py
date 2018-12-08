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

        pass

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
