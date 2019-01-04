"""mutator_gaussian.py
This file is a part of the profiling scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the fastest way to mutate with a gaussian distribution

"""
import numpy as np
import timeit
import matplotlib.pyplot as plt

def gaussian(self, array, std, boundaries, int_flag):

    nn = np.shape(array)
    # makes an array of the same size as the one given with random values\
    # pulled from a normal distribution with mean 0 and std given
    gauss_val = np.random.normal(0, std, nn)

    # creates the new mutated array with values mutated at all indices
    new_array = array + gauss_val

    # new method to handle out of bounds problem: loop around on other side
    new_array = boundaries[0, :] + ((new_array-boundaries[0, :]) %
                                    (boundaries[1, :]-boundaries[0, :]))

    # checks for flag that specifies whether output should be an integer and rounds the \
    # output arrays
    if (int_flag == True):
        new_array = (np.rint(new_array)).astype(int)

    return new_array

def gaussian_old(self, array, std, boundaries, int_flag):  # Paul

    nn = np.shape(array)
    # makes an array of the same size as the one given with random values\
    # pulled from a normal distribution with mean 0 and std given
    gauss_val = np.random.normal(0, std, nn)

    # creates the new mutated array with values mutated at all indices
    new_array = array + gauss_val

    # new method to handle out of bounds problem: loop around on other side
    for j in range(nn[-1]):
        for i in range(nn[0]):
            while (new_array[i, j] < boundaries[0, j]):
                if (new_array[i, j] < boundaries[0, j] and boundaries[0,j] != 0):
                    new_array[i, j] = boundaries[1, j] - \
                                      abs(new_array[i, j] % boundaries[0, j])
                elif (new_array[i, j] < boundaries[0, j] and boundaries[0, j] == 0):
                    new_array[i, j] = boundaries[1, j] - abs(new_array[i, j])

            while (new_array[i, j] > boundaries[1, j]):
                if (new_array[i, j] > boundaries[1, j] and boundaries[1, j] != 0):
                    new_array[i, j] = boundaries[0, j] + \
                                      abs(new_array[i, j] % boundaries[1, j])
                elif (new_array[i, j] > boundaries[1, j] and boundaries[1, j] == 0):
                    new_array[i, j] = boundaries[0, j] + abs(new_array[i, j])

    # checks for flag that specifies whether output should be an integer and rounds the \
    # output arrays
    if (int_flag == True):
        new_array = (np.rint(new_array)).astype(int)

    return new_array


a = np.linspace(5, 100, 20, dtype=int)
t_new = np.zeros(shape=a.shape)
t_old = np.zeros(shape=a.shape)

for i in range(len(a)):
    TEST_CODE = '''
array = np.random.uniform(-10.0, 10.0, ['''+str(a[i])+''', 3])
gaussian_params = {'boundaries': np.array(
[[0, -10, -5], [10, 0, 5]]), 'int_flag': False, 'std': 0.5}
child = gaussian(None, array, **gaussian_params)
'''
    t_new[i] = timeit.timeit(stmt = TEST_CODE, number = 100, globals=globals())
    

for i in range(len(a)):
    TEST_CODE_OLD = '''
array = np.random.uniform(-10.0, 10.0, ['''+str(a[i])+''', 3])
gaussian_params = {'boundaries': np.array(
[[0, -10, -5], [10, 0, 5]]), 'int_flag': False, 'std': 0.5}
child = gaussian_old(None, array, **gaussian_params)
'''
    t_old[i] = timeit.timeit(stmt = TEST_CODE_OLD, number = 100, globals=globals())
    

# plotting the data
p1 = plt.figure(1)
plt.plot(a, t_new, 'g^', a, t_old, 'rs')
plt.ylabel('Time (s)', fontsize=14)
plt.xlabel('Length of the array tested', fontsize=14)
plt.axis([0, 105, 0, 0.225])
p1.show()

p2 = plt.figure(2)
plt.loglog(a, t_new, 'g^', a, t_old, 'rs')
plt.ylabel('Time (s)', fontsize=14)
plt.xlabel('Length of the array tested', fontsize=14)
p2.show()

input()
