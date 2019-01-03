"""mutator_pseudo_bit_flip.py
This file is a part of the testing scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the fastest way to pseudo-bit-flip

"""
import numpy as np
import timeit
nn = int(1e2)
array = np.ones((nn,3))
bit_flip_params = {'boundaries' : np.array([[0,0,0],[10,10,10]]), 'proportions' : 0.5, 'int_flag' : False}

setup ='''
import numpy as np
from __main__ import method1, method2
nn = int(1e2)
array = np.ones((nn,3))
bit_flip_params = {'boundaries' : np.array([[0,0,0],[10,10,10]]), 'proportions' : 0.5, 'int_flag' : False}
'''

def method1(array,bit_flip_params):

    boundaries = bit_flip_params['boundaries']
    proportions = bit_flip_params['proportions']

    (array_row,array_col) = array.shape
    prob_mat = np.zeros(array.shape)

    for j in range(array_col):
        lower_bound, upper_bound = boundaries[0,j], boundaries[1,j]
        prob_mat[:,j] = np.random.uniform(lower_bound,upper_bound,len(array[:,j]))
        for i in range(array_row):
            if prob_mat[i,j]>array[i,j]:
                array[i,j] = np.random.uniform(lower_bound,upper_bound)

    if (bit_flip_params['int_flag'] == True):
        array = (np.floor(array)).astype(int)

    return array

def method2(array,bit_flip_params):

    boundaries = bit_flip_params['boundaries']
    proportions = bit_flip_params['proportions']

    B = np.random.choice([0, 1], size=array.shape, p=[1.-proportions, proportions])
    M = np.random.uniform(boundaries[0, :], boundaries[1, :], array.shape)
    child = np.multiply(B, M)+np.multiply((np.ones(array.shape)-B), array)

    if (bit_flip_params['int_flag'] == True):
        child = (np.floor(child)).astype(int)

    return child

child1 = method1(array,bit_flip_params)
child2 = method2(array,bit_flip_params)

test1 = '''child1 = method1(array,bit_flip_params)'''
test2 = '''child2 = method2(array,bit_flip_params)'''

ntests = int(1e3)

time1 = timeit.timeit(setup=setup,stmt=test1,number=ntests)
time2 = timeit.timeit(setup=setup,stmt=test2,number=ntests)

print('method1: ' + str(time1))
print('method2: ' + str(time2))
