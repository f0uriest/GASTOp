import numpy as np
import timeit

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


a = np.linspace(10, 100, 10, dtype=int)
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
    print("t_new %d: %f\n" %(i, t_new[i]))

for i in range(len(a)):
    TEST_CODE_OLD = '''
array = np.random.uniform(-10.0, 10.0, ['''+str(a[i])+''', 3])
gaussian_params = {'boundaries': np.array(
[[0, -10, -5], [10, 0, 5]]), 'int_flag': False, 'std': 0.5}
child = gaussian_old(None, array, **gaussian_params)
'''
    t_old[i] = timeit.timeit(stmt = TEST_CODE_OLD, number = 100, globals=globals())
    print("t_old %d: %f\n" %(i, t_old[i]))
