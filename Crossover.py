import numpy as np

class Crossover():

# Crossover() object takes in two parents and returns two children

    def __init__(self,crossover_params):
        self.params = crossover_params

    def uniform_crossover(self, truss_1, truss_2 ,uniform_crossover_params=None): #Paul "gosh dog" kaneelil
        ''' (aka uniform crossover)
        For each array, generate another array of 0s and 1s. If its a 0, take
        data from one parent and if its a 1, take data from the other parent.
        Let's say parent one corresponds to 0 and parent two to 1:
        To make normal child, multiply array of 0s and 1s with parent two array
        and the complement of that 0s and 1s array with parent one array and
        add the two resulting arrays together.
        To make the evil kid, do the opposite.
        Output 2 children
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
        child1 = (unos_and_zeros * truss_2) + (unos_and_zeros_c * truss_2)
        child2 = (unos_and_zeros_c * truss_2) + (unos_and_zeros * truss_2)

        return child1, child2

    def single_point_split(self, array_1, array_2, single_point_split_params=None): #Amlan
        '''
        Look up the exact algorithm, but it goes something like this
        Given a point in the array where you want to split the data (google how
        to choose that point). For the first child, once you have a splitting
        point, take the things from truss 1 up to that point and append the
        things from truss 2 after that point. Do the opposite for the other
        children.
        '''
        '''
        Nodes_1 = truss_1.nodes
        Nodes_2 = truss_2.nodes
        i = self.params['node_crossover']
        Edges_1 = truss_1.edges
        Edges_2 = truss_2.edges
        j = self.params['edge_crossover']
        Properties_1 = truss_1.properties
        Properties_2 = truss_2.properties
        k = self.params['property_crossover']

        truss_1.nodes = np.concatenate((Nodes_1[:i],Nodes_2[i:]),axis=0)
        truss_2.nodes = np.concatenate((Nodes_2[:i],Nodes_1[i:]),axis=0)

        truss_1.edges = np.concatenate((Edges_1[:j],Edges_2[j:]),axis=0)
        truss_2.edges = np.concatenate((Edges_2[:j],Edges_1[j:]),axis=0)

        truss_1.properties = np.concatenate((Properties_1[:k],Properties_2[k:]),axis=0)
        truss_2.properties = np.concatenate((Properties_2[:k],Properties_1[k:]),axis=0)
        '''

        (array_row,array_col) = array_1.shape
        point = np.random.randint(0, array_row)

        child_1 = np.concatenate((array_1[:point],array_2[point:]),axis=0)
        child_2 = np.concatenate((array_2[:point],array_1[point:]),axis=0)

        return child_1, child_2

        # pass

    def __call__(self,truss_1,truss_2):

        node_method = getattr(self,self.params['node_crossover'])
        edge_method = getattr(self,self.params['edge_crossover'])
        property_method = getattr(self,self.params['property_crossover'])

        truss.nodes = node_method(truss_1.nodes,truss_2.nodes,self.params['nodes'])
        truss.edges = edge_method(truss_1.edges,truss_2.edges,self.params['edges'])
        truss.properties = property_method(truss_1.properties,truss_2.properties,self.params['properties'])

        return truss
