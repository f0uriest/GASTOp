# testing fastest way to construct stiffness matrices
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
    azim = np.arctan2(y, x)
    elev = np.pi/2 - np.arccos(z/r)

    return r, elev, azim


def method1(edge_vec):

    L, b, a = cart2sph(edge_vec[:, 0], edge_vec[:, 1], edge_vec[:, 2])
    ca = np.cos(a)  # a is azimuthal angle
    sa = np.sin(a)
    cb = np.cos(b)  # b is elevation angle
    sb = np.sin(b)
    return ca, sa, cb, sb


def method2(edge_vec):
    rho = np.sqrt(edge_vec[:, 0]**2+edge_vec[:, 1]**2)
    L = np.sqrt(rho**2 + edge_vec[:, 2]**2)
    ca = edge_vec[:, 0]/rho
    sa = edge_vec[:, 1]/rho
    cb = rho/L
    sb = edge_vec[:, 2]/L
    return ca, sa, cb, sb


ca1, sa1, cb1, sb1 = method1(edge_vec)
ca2, sa2, cb2, sb2 = method2(edge_vec)


np.testing.assert_array_almost_equal(ca1, ca2)
np.testing.assert_array_almost_equal(sa1, sa2)
np.testing.assert_array_almost_equal(cb1, cb2)
np.testing.assert_array_almost_equal(sb1, sb2)

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
