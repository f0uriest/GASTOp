"""local_stiffness.py
This file is a part of the profiling scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements testing for the fastest way to construct stiffness matrices

"""
import numpy as np
import timeit
num_con = 50
E = np.random.random(num_con)
A = np.random.random(num_con)
L = np.random.random(num_con)
Iz = np.random.random(num_con)
Iy = np.random.random(num_con)
G = np.random.random(num_con)
J = np.random.random(num_con)

setup = '''
import numpy as np
from __main__ import method1, method2
num_con = 50
E = np.random.random(num_con)
A = np.random.random(num_con)
L = np.random.random(num_con)
Iz = np.random.random(num_con)
Iy = np.random.random(num_con)
G = np.random.random(num_con)
J = np.random.random(num_con)
'''


def method1(num_con, E, A, L, Iz, Iy, G, J):
    k1 = np.zeros((3, 3, num_con))  # stiffness matrix components
    k2 = np.zeros((3, 3, num_con))  # stiffness matrix components
    k3 = np.zeros((3, 3, num_con))  # stiffness matrix components
    k4 = np.zeros((3, 3, num_con))  # stiffness matrix components
    Kloc = np.zeros((12, 12, num_con))

    # stiffness matrix elements in x,y,z,theta
    co = np.stack((12*np.ones(num_con), 6*L, 4*L**2, 2*L**2), axis=1)
    x = (E*A)/L  # axial stiffness along x
    y = (((E*Iy)/(L**3))*co.T).T  # bending stiffness about y
    z = (((E*Iz)/(L**3))*co.T).T  # bending stiffness about z
    g = G*J/L  # torsional stiffness about x axis

    # form stacked local stiffness matrices
    k1[0, 0, :] = x
    k1[1, 1, :] = z[:, 0]
    k1[2, 2, :] = y[:, 0]
    k2[1, 2, :] = z[:, 1]
    k2[2, 1, :] = -y[:, 1]
    k3[0, 0, :] = g
    k3[1, 1, :] = y[:, 2]
    k3[2, 2, :] = z[:, 2]
    k4[0, 0, :] = -g
    k4[1, 1, :] = y[:, 3]
    k4[2, 2, :] = z[:, 3]
    k2t = np.transpose(k2, axes=(1, 0, 2))
    kr1 = np.concatenate((k1, k2, -k1, k2), axis=1)
    kr2 = np.concatenate((k2t, k3, -k2t, k4), axis=1)
    kr3 = np.concatenate((-k1, -k2, k1, -k2), axis=1)
    kr4 = np.concatenate((k2t, k4, -k2t, k3), axis=1)
    Kloc = np.concatenate((kr1, kr2, kr3, kr4), axis=0)

    return Kloc


def method2(num_con, E, A, L, Iz, Iy, G, J):
    k1 = np.zeros((3, 3, num_con))  # stiffness matrix components
    k2 = np.zeros((3, 3, num_con))  # stiffness matrix components
    k3 = np.zeros((3, 3, num_con))  # stiffness matrix components
    k4 = np.zeros((3, 3, num_con))  # stiffness matrix components
    Kloc = np.zeros((12, 12, num_con))

    # stiffness matrix elements in x,y,z,theta
    co = np.stack((12*np.ones(num_con), 6*L, 4*L**2, 2*L**2), axis=1)
    x = (E*A)/L  # axial stiffness along x
    y = (((E*Iy)/(L**3))*co.T).T  # bending stiffness about y
    z = (((E*Iz)/(L**3))*co.T).T  # bending stiffness about z
    g = G*J/L  # torsional stiffness about x axis

    # form stacked local stiffness matrices
    k1[0, 0, :] = x
    k1[1, 1, :] = z[:, 0]
    k1[2, 2, :] = y[:, 0]
    k2[1, 2, :] = z[:, 1]
    k2[2, 1, :] = -y[:, 1]
    k3[0, 0, :] = g
    k3[1, 1, :] = y[:, 2]
    k3[2, 2, :] = z[:, 2]
    k4[0, 0, :] = -g
    k4[1, 1, :] = y[:, 3]
    k4[2, 2, :] = z[:, 3]
    k2t = np.transpose(k2, axes=(1, 0, 2))

    Kloc[0:3, 0:3, :] = k1
    Kloc[0:3, 3:6, :] = k2
    Kloc[0:3, 6:9, :] = -k1
    Kloc[0:3, 9:12, :] = k2
    Kloc[3:6, 0:3, :] = k2t
    Kloc[3:6, 3:6, :] = k3
    Kloc[3:6, 6:9, :] = -k2t
    Kloc[3:6, 9:12, :] = k4
    Kloc[6:9, 0:3, :] = -k1
    Kloc[6:9, 3:6, :] = -k2
    Kloc[6:9, 6:9, :] = k1
    Kloc[6:9, 9:12, :] = -k2
    Kloc[9:12, 0:3, :] = k2t
    Kloc[9:12, 3:6, :] = k4
    Kloc[9:12, 6:9, :] = -k2t
    Kloc[9:12, 9:12, :] = k3

    return Kloc


K1 = method1(num_con, E, A, L, Iz, Iy, G, J)
K2 = method2(num_con, E, A, L, Iz, Iy, G, J)


np.testing.assert_array_almost_equal(K1, K2)


test1 = '''K1 = method1(num_con, E, A, L, Iz, Iy, G, J)'''
test2 = '''K2 = method2(num_con, E, A, L, Iz, Iy, G, J)'''


ntests = 10000

time1 = timeit.timeit(setup=setup,
                      stmt=test1,
                      number=ntests)


time2 = timeit.timeit(setup=setup,
                      stmt=test2,
                      number=ntests)


print('method1: ' + str(time1))
print('method2: ' + str(time2))
