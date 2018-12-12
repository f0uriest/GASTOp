import unittest
import numpy as np

import Mutator

'''
# pseudo test code
array = np.arange(1,11,1).reshape((10,1))
bit_flip_params = np.array([[0],[10]])
myMutator = Mutator.Mutator([])
new_array = myMutator.pseudo_bit_flip(array,bit_flip_params)

print(new_array)
'''

class TestMutator_pseudo_bit_flip(unittest.TestCase):
    def testBasic(self):
        array = np.arange(1,31,1).reshape((10,3))
        bit_flip_params = [[0,0,0],[10,10,10]]
        myMutator = Mutator.Mutator([])
        child_1 = myMutator.pseudo_bit_flip(array,bit_flip_params)
