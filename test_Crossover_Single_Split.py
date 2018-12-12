import unittest
import numpy as np

import Crossover

'''
array1 = np.arange(1,11,1).reshape((10,1))
array2 = np.arange(11,21,1).reshape((10,1))
myCrossover = Crossover.Crossover([])
child_1, child_2 = myCrossover.single_point_split(array1,array2)
print('child_1 =\n',child_1)
print('child_2 =\n',child_2)
'''

class TestCrossover_singlepointsplit(unittest.TestCase):
    def test_Basic(self):
        array1 = np.arange(1,11,1).reshape((10,1))
        array2 = np.arange(11,21,1).reshape((10,1))
        myCrossover = Crossover.Crossover([])
        child_1 = myCrossover.single_point_split(array1,array2)

        np.testing.assert_array_equal(child_1,np.array([1,2,3,4,5,16,17,18,19,20]))
        np.testing.assert_array_equal(child_2,np.array([11,12,13,14,15,6,7,8,9,10]))

if __name__ == '__main__':
    unittest.main()
