from multiprocessing import Pool
import numpy.testing as npt
import numpy as np


class Plus():
    def __init__(self, x):
        self.x = x

    def bar(self, y):
        return self.x+y

    def __call__(self, y):
        #        return self.bar(y)
        y = self.bar(y)


class Power():
    def __init__(self, pow):
        self.pow = pow

    def foo(self, x):
        return x**self.pow

    def __call__(self, y):
        return self.foo(y)


L = [i for i in range(1000000)]
L2 = (np.array(L)+1)**2

power = Power(2)
plus = Plus(1)

pool = Pool()
L = pool.map(plus, L)
pool.close()
pool.join()

pool = Pool()
L = pool.map(power, L)
pool.close()
pool.join()

npt.assert_array_almost_equal(L, L2)
