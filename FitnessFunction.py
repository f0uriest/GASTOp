import Truss
import numpy as np


class FitnessFunction():  # Rory
    # equation: string flag to denote which hard-coded method to use
    # weights: numpy array

    def __init__(self, equation, parameters):
        self.equation = equation  # function handle
        self.parameters = parameters  # list

    def sphere(self, truss):
        '''sum of squares of node array elements. ie, sphere function
        global min at x = 0 where f = 0
        '''
        x = truss.nodes.flatten()
        f = np.sum(x**2)
        return f

    def rosenbrock(self, truss):
        '''n dimensional rosenbrock function using N/2 formulation
        f(x) = Sum(100*(x[2i-1]^2 - x[2i]^2)^2 + (x[2i-1] - 1)^2) for i=1 to N/2
        global minimum at x = (1,1,1,....) where f = 0
        '''
        x = truss.nodes.flatten()
        if x.size % 2:
            x = x[1:]  # need an even number of elements
        N = x.size
        f = 0
        for i in range(int(N/2)):
            f += 100*(x[2*i]**2 - x[2*i+1])**2 + (x[2*i] - 1)**2
        return f

    def rastrigin(self, truss):
        '''n-dimensional Restrigin function
        f(x) = An + Sum(x_i^2 -Acos(2pi*x_i)) for i=1 to N
        n determined from size of nodes array
        x_i are entries of node array
        global min at x=0 where f=0
        '''
        A = 10
        x = truss.nodes.flatten()
        n = x.size
        x2 = x**2
        cosx = np.cos(2*np.pi*x)
        f = A*n + np.sum(x2-A*cosx)
        return f

    def __call__(self, truss):
        equation = getattr(self, self.equation)
        f = equation(truss)
        truss.fitness_score = f
