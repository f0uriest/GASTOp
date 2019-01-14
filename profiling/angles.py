"""angles.py
This file is a part of the profiling scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements tests for angle calculations

"""
import numpy as np
import timeit

setup = '''
import numpy as np
from __main__ import cart2sph, method1, method2
edge_vec = np.random.random((20,3))
'''
edge_vec = np.random.random((40, 3))


def cart2sph(x, y, z):
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    r = np.sqrt(x**2+y**2+z**2)
    azim = np.arctan2(z, x)
    elev = np.pi/2 - np.arccos(y/r)

    return r, elev, azim


def method1(edge_vec):

    L, b, a = cart2sph(edge_vec[:, 0], edge_vec[:, 1], edge_vec[:, 2])
    ca = np.cos(a)  # a is azimuthal angle
    sa = np.sin(a)
    cb = np.cos(b)  # b is elevation angle
    sb = np.sin(b)
    return ca, sa, cb, sb


def method2(edge_vec):
    eps = 1e-16
    rho = np.sqrt(edge_vec[:, 0]**2+edge_vec[:, 2]**2)
    L = np.sqrt(rho**2 + edge_vec[:, 1]**2)
    sing = rho < eps
    edge_vec[:, 0][sing] = 1
    edge_vec[:, 2][sing] = 0
    rho[sing] = 1
    ca = edge_vec[:, 0]/rho
    sa = edge_vec[:, 2]/rho
    rho[sing] = 0
    cb = rho/L
    sb = edge_vec[:, 1]/L
    return ca, sa, cb, sb


cas1, sas1, cbs1, sbs1 = method1(np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]]))
cas2, sas2, cbs2, sbs2 = method2(np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]]))
ca1, sa1, cb1, sb1 = method1(edge_vec)
ca2, sa2, cb2, sb2 = method2(edge_vec)


np.testing.assert_array_almost_equal(ca1, ca2)
np.testing.assert_array_almost_equal(sa1, sa2)
np.testing.assert_array_almost_equal(cb1, cb2)
np.testing.assert_array_almost_equal(sb1, sb2)
np.testing.assert_array_almost_equal(
    [cas1, sas1, cbs1, sbs1], [cas2, sas2, cbs2, sbs2])

test1 = '''ca1,sa1,cb1,sb1 = method1(edge_vec)'''
test2 = '''ca2,sa2,cb2,sb2 = method2(edge_vec)'''


ntests = 100000

time1 = timeit.timeit(setup=setup,
                      stmt=test1,
                      number=ntests)


time2 = timeit.timeit(setup=setup,
                      stmt=test2,
                      number=ntests)

print('method1: ' + str(time1))
print('method2: ' + str(time2))
