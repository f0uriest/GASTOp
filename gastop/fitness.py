import numpy as np


class FitnessFunction():

    def __init__(self, equation, parameters):
        self.equation = getattr(self, equation)
        self.parameters = parameters  # dictionary

    def weighted_sum(self, truss, parameters):
        """Computes fitness score using a weighted sum of mass and fos

        Args:
            truss (Truss object): truss to be scored. Must have mass
                fos attributes defined (for example, by using evaluator).
            parameters (dict): Dictionary with the following entries:
                'goal_fos' (float >= 0) : desired factor of safety. Trusses with
                    a smaller fos will be penalized according to 'w_fos'
                'critical_nodes' (int, array): Array of nodes #s for which 
                    deflection should be minimized. If empty, defaults to all.
                'w_fos' (float >= 0): penalty weight for low fos. Only applied
                    if fos < goal_fos
                'w_mass' (float >= 0): weight penalty applied to mass. Relative
                    magnitude of 'w_mass' and 'w_fos' determines importance of
                    minimizing mass vs maximizing fos.
                'w_deflection' (float >=0, array): penalty applied to deflections
                    If scalar, applies the same penalty to all critical nodes.
                    Can also be an array the same size as 'critical_nodes' in 
                    which case different penalties will be applied to each node.
        Returns:
            f (float): Fitness score. Computed as:
                f = w_mass*mass + w_fos*max(goal_fos-min_fos, 0)
                    + w_deflection*deflection[critical_nodes]
                min_fos is the lowest fos for structure under all loads.
                If min_fos > goal_fos, no fos penalty applied, so f 
                depends only on mass.
        """

        if truss.fos.size:
            minfos = truss.fos.min()
        else:
            minfos = 0

        if self.parameters['critical_nodes'].size:
            deflections = truss.deflection[self.parameters['critical_nodes']][:, :3]
        else:
            deflections = truss.deflection[:, :3]

        deflection_score = np.sum(
            self.parameters['w_deflection']*np.sqrt(np.sum(deflections**2)))
        fs = np.maximum(self.parameters['goal_fos'] - minfos, 0)
        f = self.parameters['w_mass']*truss.mass + \
            self.parameters['w_fos']*fs + deflection_score
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

        x = truss.rand_nodes.flatten()
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

        x = truss.rand_nodes.flatten()
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
        x = truss.rand_nodes.flatten()
        n = x.size
        x2 = x**2
        cosx = np.cos(2*np.pi*x)
        f = A*n + np.sum(x2-A*cosx)
        return f

    def __call__(self, truss):
        f = self.equation(truss, self.parameters)
        truss.fitness_score = f
