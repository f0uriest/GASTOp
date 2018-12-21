import Truss
import numpy as np


class FitnessFunction():

    def __init__(self, equation, parameters):
        self.equation = equation  # string function handle
        self.parameters = parameters  # dictionary

    def weighted_sum(self, truss, parameters):
        """Computes fitness score using a weighted sum of mass and fos

        Args:
            truss (Truss object): truss to be scored. Must have mass
                fos attributes defined (for example, by using evaluator).
            parameters (dict): Dictionary with the following entries:
                'goal_fos' (float >= 0) : desired factor of safety. Trusses with
                    a smaller fos will be penalized according to 'w_fos'
                'w_fos' (float >= 0): penalty weight for low fos. Only applied
                    if fos < goal_fos
                'w_mass' (float >= 0): weight penalty applied to mass. Relative
                    magnitude of 'w_mass' and 'w_fos' determines importance of
                    minimizing mass vs maximizing fos.
        Returns:
            f (float): Fitness score. Computed as:
                f = w_mass*mass + w_fos*max(goal_fos-min_fos, 0)
                min_fos is the lowest fos for structure under all loads.
                If min_fos > goal_fos, no fos penalty applied, so f 
                depends only on mass.
        """

        minfos = truss.fos.min()
        fs = np.maximum(self.parameters['goal_fos'] - minfos, 0)
        f = self.parameters['w_mass']*truss.mass + self.parameters['w_fos']*fs
        return f

    def sphere(self, truss, parameters=None):
        """Sum of squares of node array elements. aka, sphere function

        Global min at x = 0 where f = 0

        Args: 
            truss (Truss object): only uses truss object as container for 
                nodes. No other attributes needed.
            parameters (dict): None needed for this method

        Returns:
            f (float): fitness score. Computed as
                f(x) = Sum(x[i]**2) for i=1 to n
                n determined from size of nodes array
                x_i are entries of node array
        """

        x = truss.nodes.flatten()
        f = np.sum(x**2)
        return f

    def rosenbrock(self, truss, parameters=None):
        """n-dimensional Rosenbrock function

        Sum of n/2 2D Rosenbrock functions
        Global min at x=1 where f=0

        Args: 
            truss (Truss object): only uses truss object as container for 
                nodes. No other attributes needed.
            parameters (dict): None needed for this method

        Returns:
            f (float): fitness score. Computed as
                f(x) = Sum(100*(x[2i-1]^2 - x[2i]^2)^2 + (x[2i-1] - 1)^2)
                for i=1 to n/2
                n determined from size of nodes array
                x_i are entries of node array
        """

        x = truss.nodes.flatten()
        if x.size % 2:
            x = x[1:]  # need an even number of elements
        n = x.size
        f = 0
        for i in range(int(n/2)):
            f += 100*(x[2*i]**2 - x[2*i+1])**2 + (x[2*i] - 1)**2
        return f

    def rastrigin(self, truss, parameters=None):
        """n-dimensional Restrigin function

        Global min at x=0 where f=0

        Args: 
            truss (Truss object): only uses truss object as container for 
                nodes. No other attributes needed.
            parameters (dict): None needed for this method

        Returns:
            f (float): fitness score. Computed as
                f(x) = A*n + Sum(x_i^2 -A*cos(2*pi*x_i)) for i=1 to n
                n determined from size of nodes array
                x_i are entries of node array
        """

        A = 10  # normalizing parameters
        x = truss.nodes.flatten()
        n = x.size
        x2 = x**2
        cosx = np.cos(2*np.pi*x)
        f = A*n + np.sum(x2-A*cosx)
        return f

    def __call__(self, truss):
        equation = getattr(self, self.equation)
        f = equation(truss, self.parameters)
        truss.fitness_score = f
