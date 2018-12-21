#!/usr/bin/env python3

import unittest
import numpy as np

import Mutator

class TestMutator_pseudo_bit_flip(unittest.TestCase):

    def test_basic(self):
        array = np.ones((10,3))
        bit_flip_params = {'boundaries' : np.array([[0,0,0],[10,10,10]]), 'proportions' : 0.5, 'int_flag' : False}
        myMutator = Mutator.Mutator([])
        child = myMutator.pseudo_bit_flip(array,bit_flip_params)

    def test_datatype(self):
        array = np.ones((10,3))
        bit_flip_params = {'boundaries' : np.array([[0,0,0],[10,10,10]]), 'proportions' : 0.5, 'int_flag' : True}
        myMutator = Mutator.Mutator([])
        child = myMutator.pseudo_bit_flip(array,bit_flip_params)

        np.testing.assert_string_equal(str(child.dtype), 'int64')

if __name__ == '__main__':
    unittest.main()
