"""rotation_matrices.py
This file is a part of the profiling scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the fastest way to build stacked rotation and transformation matrices

"""
import numpy as np
import timeit
num_con = 20
ca = np.random.random(num_con)
cb = np.random.random(num_con)
sa = np.random.random(num_con)
sb = np.random.random(num_con)

setup = '''
import numpy as np
from __main__ import direct_assignment, nparray, concat
num_con = 20
ca = np.random.random(num_con)
cb = np.random.random(num_con)
sa = np.random.random(num_con)
sb = np.random.random(num_con)
'''


def nparray(ca, cb, sa, sb):
    r = np.array([[cb*ca, sb, sa*cb], [-sb*ca, cb, -sb*sa],
                  [-sa, np.zeros(ca.shape), ca]])
    T = np.kron(np.eye(4).reshape(4, 4, 1), r)
    return T


def direct_assignment(ca, cb, sa, sb):
    r = np.zeros((3, 3, num_con))
    T = np.zeros((12, 12, num_con))
    r[0, 0, :] = cb*ca
    r[0, 1, :] = sb
    r[0, 2, :] = sa*cb
    r[1, 0, :] = -sb*ca
    r[1, 1, :] = cb
    r[1, 2, :] = -sb*sa
    r[2, 0, :] = -sa
    r[2, 2, :] = ca
    T[0:3, 0:3, :] = r
    T[3:6, 3:6, :] = r
    T[6:9, 6:9, :] = r
    T[9:12, 9:12, :] = r
    return T


def concat(ca, cb, sa, sb):
    ca = ca.reshape(1, 1, *ca.shape)
    cb = cb.reshape(1, 1, *cb.shape)
    sa = sa.reshape(1, 1, *sa.shape)
    sb = sb.reshape(1, 1, *sb.shape)
    rr1 = np.concatenate((cb*ca, sb, sa*cb), axis=1)
    rr2 = np.concatenate((-sb*ca, cb, -sb*sa), axis=1)
    rr3 = np.concatenate((-sa, np.zeros(ca.shape), ca), axis=1)
    r = np.concatenate((rr1, rr2, rr3), axis=0)
    z = np.zeros(r.shape)
    Tr1 = np.concatenate((r, z, z, z), axis=1)
    Tr2 = np.concatenate((z, r, z, z), axis=1)
    Tr3 = np.concatenate((z, z, r, z), axis=1)
    Tr4 = np.concatenate((z, z, z, r), axis=1)
    T = np.concatenate((Tr1, Tr2, Tr3, Tr4), axis=0)
    return T


T1 = nparray(ca, cb, sa, sb)
T2 = direct_assignment(ca, cb, sa, sb)
T3 = concat(ca, cb, sa, sb)

np.testing.assert_array_almost_equal(T1, T2)
np.testing.assert_array_almost_equal(T1, T3)


test1 = '''T1 = nparray(ca,cb,sa,sb)'''
test2 = '''T2 = direct_assignment(ca,cb,sa,sb)'''
test3 = '''T3 = concat(ca,cb,sa,sb)'''

ntests = 100000

time1 = timeit.timeit(setup=setup,
                      stmt=test1,
                      number=ntests)


time2 = timeit.timeit(setup=setup,
                      stmt=test2,
                      number=ntests)

time3 = timeit.timeit(setup=setup,
                      stmt=test3,
                      number=ntests)

print('nparray: ' + str(time1))
print('direct assigment: ' + str(time2))
print('concat: ' + str(time3))
