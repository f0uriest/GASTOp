"""crossover.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the crossover class.

"""
import numpy as np
from gastop import Truss


class Crossover():

    '''

    Mixes attributes belonging to two different parents to produce two children with
    specific characteristics from both parents.

    When creating a new Crossover() obejct, must be initialized with dictionary
    crossover_params (containing crossover method). Object can then be used as a
    function that produces children according to the specified method.



    '''

    def __init__(self, crossover_params):
        """Creates Crossover object.

        Once instantiated, the Crossover object can be called as a function
        to combine two trusses using the specified methods and parameters.

        Args: 
            crossover_params (dict): Dictionary containing:

                - ``'node_crossover_method'`` *(str)*: Name of method to use for
                  node crossover.
                - ``'edge_crossover_method'`` *(str)*: Name of method to use for
                  edge crossover.
                - ``'property_crossover_method'`` *(str)*: Name of method to use
                  for property crossover.
                - ``'user_spec_nodes'`` *(ndarray)*: Array of user specified nodes
                  that should be passed on unaltered.

        Returns:
            Crossover callable object.

        """
        self.params = crossover_params
        self.node_method = getattr(self, self.params['node_crossover_method'])
        self.edge_method = getattr(self, self.params['edge_crossover_method'])
        self.property_method = getattr(
            self, self.params['property_crossover_method'])

    @staticmethod
    def uniform_crossover(parent_1, parent_2):  # Paul
        '''Performs a uniform crossover on the two parents

        The uniform crossover method creates two child arrays by randomly mixing together
        information taken from two parent arrays. To do this, the method creates two arrays
        of ones and zeros -one being the complement of the other- with the same shape as
        the parent arrays. The first array is multiplied with parent1 and the complementary
        array is multiplied with parent2 before adding the results together to make child1.
        The exact opposite multiplication is done to make child2.

        Args:
            parent_1 (ndarray): Numpy array containing information for parent 1.
            parent_2 (ndarray): Numpy array containing information for parent 2.

        Returns:
            child1, child2 (ndarrays): Numpy arrays containing information for children.

        '''
        # find the shape of the parents
        nn = np.shape(parent_1)

        # making an array of ones and zeros
        unos_and_zeros = np.random.randint(2, size=nn)

        # creating an array of all ones to later create the complementary array
        unos = np.ones(nn, dtype=int)

        # creating the complementary array
        unos_and_zeros_c = unos - unos_and_zeros

        # making kids ;)
        child1 = (unos_and_zeros * parent_1) + (unos_and_zeros_c * parent_2)
        child2 = (unos_and_zeros_c * parent_1) + (unos_and_zeros * parent_2)

        return child1, child2

    @staticmethod
    def single_point_split(array_1, array_2):  # Amlan
        '''
        Performs a single point split crossover between two parents

        It takes specific information from two parents and returns two children
        containing characteristics from both parents. In order to achieve this,
        it chooses a random point and splits the two parents into two different
        parts. Then it merges the first half of the first parent with the second
        half of the second parent and vice versa.

        Args:
            array_1 (ndarray): Numpy array containing information for parent 1.
            array_2 (ndarray): Numpy array containing information for parent 2.

        Returns:
            child1, child2 (ndarrays): Numpy arrays containing information for children.

       '''

        # Choosing a random point
        array_row = len(array_1)
        point = np.random.randint(0, array_row)

        # Mixing the two parents
        child_1 = np.concatenate((array_1[:point], array_2[point:]), axis=0)
        child_2 = np.concatenate((array_2[:point], array_1[point:]), axis=0)

        return child_1, child_2

    @staticmethod
    def two_points_split(array_1, array_2):  # Amlan
        '''

        Takes specific values of two parents and return two children containing
        characteristics from both parents.

        Chooses two random points and splits the two parents into three different parts.
        Replaces the central part of the first parent with the central part of the second
        parent.

        Args:
            array_1 (ndarray): Numpy array containing information for parent 1.
            array_2 (ndarray): Numpy array containing information for parent 2.

        Returns:
            child_1, child_2 (ndarrays): Numpy arrays containing information for children.

        '''
        # Choosing two random points
        p1 = np.random.randint(1, len(array_1))
        p2 = np.random.randint(1, len(array_1)-1)

        # Preparing the two points such that p1<p2
        if p2 >= p1:
            p2 += 1
        else:
            p1, p2 = p2, p1

        # # Mixing the two parents
        child_1 = array_1
        child_2 = array_2
        child_1[p1:p2, :], child_2[p1:p2,
                                   :] = child_2[p1:p2, :], child_1[p1:p2, :]

        return child_1, child_2

    def __call__(self, truss_1, truss_2):
        """Calls a crossover object on two trusses to combine them.

        Crossover object must have been instantiated specifying which
        methods to use.

        Args:
            truss_1 (Truss object): First truss to be combined.
            truss_2 (Truss object): Second truss to be combined.

        Returns:
            child_1, child_2 (Truss objects): Child trusses produced by crossover.

        """

        user_spec_nodes = self.params['user_spec_nodes']
        child_1 = Truss(user_spec_nodes, 0, 0, 0)
        child_2 = Truss(user_spec_nodes, 0, 0, 0)
        child_1.rand_nodes, child_2.rand_nodes = self.node_method(
            truss_1.rand_nodes, truss_2.rand_nodes, **self.params['node_crossover_params'])
        child_1.edges, child_2.edges = self.edge_method(
            truss_1.edges, truss_2.edges, **self.params['edge_crossover_params'])
        child_1.properties, child_2.properties = self.property_method(
            truss_1.properties, truss_2.properties, **self.params['property_crossover_params'])

        return child_1, child_2
