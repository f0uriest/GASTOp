"""mutator_pseudo_bit_flip.py
This file is a part of the profiling scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the fastest way to pseudo-bit-flip

"""
import numpy as np
import matplotlib.pyplot as plt

import timeit

nn_1 = int(1e1)
nn_2 = int(1e2)
nn_3 = int(1e3)
nn_4 = int(1e4)
nn_5 = int(1e5)
nn_6 = int(1e6)

array_1 = np.ones((nn_1,3))
array_2 = np.ones((nn_2,3))
array_3 = np.ones((nn_3,3))
array_4 = np.ones((nn_4,3))
array_5 = np.ones((nn_5,3))
array_6 = np.ones((nn_6,3))

bit_flip_params = {'boundaries' : np.array([[0,0,0],[10,10,10]]), 'proportions' : 0.5, 'int_flag' : False}

setup ='''
import numpy as np
from __main__ import method1, method2

nn_1 = int(1e1)
nn_2 = int(1e2)
nn_3 = int(1e3)
nn_4 = int(1e4)
nn_5 = int(1e5)
nn_6 = int(1e6)

array_1 = np.ones((nn_1,3))
array_2 = np.ones((nn_2,3))
array_3 = np.ones((nn_3,3))
array_4 = np.ones((nn_4,3))
array_5 = np.ones((nn_5,3))
array_6 = np.ones((nn_6,3))

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

child_1a = method1(array_1,bit_flip_params)
child_1b = method2(array_1,bit_flip_params)
child_2a = method1(array_2,bit_flip_params)
child_2b = method2(array_2,bit_flip_params)
child_3a = method1(array_3,bit_flip_params)
child_3b = method2(array_3,bit_flip_params)
child_4a = method1(array_4,bit_flip_params)
child_4b = method2(array_4,bit_flip_params)
child_5a = method1(array_5,bit_flip_params)
child_5b = method2(array_5,bit_flip_params)
child_6a = method1(array_6,bit_flip_params)
child_6b = method2(array_6,bit_flip_params)

test_1a = '''child_1a = method1(array_1,bit_flip_params)'''
test_1b = '''child_1b = method2(array_1,bit_flip_params)'''
test_2a = '''child_2a = method1(array_2,bit_flip_params)'''
test_2b = '''child_2b = method2(array_2,bit_flip_params)'''
test_3a = '''child_3a = method1(array_3,bit_flip_params)'''
test_3b = '''child_3b = method2(array_3,bit_flip_params)'''
test_4a = '''child_4a = method1(array_4,bit_flip_params)'''
test_4b = '''child_4b = method2(array_4,bit_flip_params)'''
test_5a = '''child_5a = method1(array_5,bit_flip_params)'''
test_5b = '''child_5b = method2(array_5,bit_flip_params)'''
test_6a = '''child_6a = method1(array_6,bit_flip_params)'''
test_6b = '''child_6b = method2(array_6,bit_flip_params)'''

ntests = int(1e3)

time_1a = timeit.timeit(setup=setup,stmt=test_1a,number=ntests)
time_1b = timeit.timeit(setup=setup,stmt=test_1b,number=ntests)
print('Test 1 done')
time_2a = timeit.timeit(setup=setup,stmt=test_2a,number=ntests)
time_2b = timeit.timeit(setup=setup,stmt=test_2b,number=ntests)
print('Test 2 done')
time_3a = timeit.timeit(setup=setup,stmt=test_3a,number=ntests)
time_3b = timeit.timeit(setup=setup,stmt=test_3b,number=ntests)
print('Test 3 done')
time_4a = timeit.timeit(setup=setup,stmt=test_4a,number=ntests)
time_4b = timeit.timeit(setup=setup,stmt=test_4b,number=ntests)
print('Test 4 done')
time_5a = timeit.timeit(setup=setup,stmt=test_5a,number=ntests)
time_5b = timeit.timeit(setup=setup,stmt=test_5b,number=ntests)
print('Test 5 done')
time_6a = timeit.timeit(setup=setup,stmt=test_6a,number=ntests)
time_6b = timeit.timeit(setup=setup,stmt=test_6b,number=ntests)
print('Test 6 done')

# data to plot
n_groups = 6
tot_time_1 = (time_1a, time_2a, time_3a, time_4a, time_5a, time_6a)
tot_time_2 = (time_1b, time_2b, time_3b, time_4b, time_5b, time_6b)
#tot_time_1 = (time_1a, time_2a, time_3a, time_4a, time_5a)
#tot_time_2 = (time_1b, time_2b, time_3b, time_4b, time_5b)

size_arr = (nn_1, nn_2, nn_3, nn_4, nn_5, nn_6)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.20
opacity = 0.50

rects1 = plt.bar(index, tot_time_1, bar_width,
                 alpha=opacity,
                 color='red',
                 label='Method 1')

rects2 = plt.bar(index + bar_width, tot_time_2, bar_width,
                 alpha=opacity,
                 color='seagreen',
                 label='Method 2')

plt.xlabel('Methods')
plt.ylabel('Run times')
plt.title('Run-time dependence on the size of the arrays')
plt.xticks(index + bar_width, ('1e1', '1e2', '1e3', '1e4', '1e5', '1e6'))
plt.legend()

plt.tight_layout()
plt.show()

# create plot
fig, ax = plt.subplots()

rects1 = plt.loglog(size_arr, tot_time_1, 'ro')
rects2 = plt.loglog(size_arr, tot_time_2, 'go')

plt.xlabel('Size of the arrays')
plt.ylabel('Run times')
plt.title('Run-time dependence on the size of the arrays')
plt.show()
