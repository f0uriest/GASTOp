import numpy as np


class FitnessFunction():
    """Implements fitness functions for computing fitness scores.

    The fitness function assigns a single value to each truss based
    on various parameters, so that comparisons between trusses can be made.

    The class is designed to be instantiated as a FitnessFunction object
    which operates on Truss objects to assign a fitness score, though methods 
    from the class may also be called directly.
    """

    def __init__(self, equation, parameters):
        """Creates a FitnessFunction object

        Once created, the object acts like a function and can be called on a Truss
        object to assign it a fitness score.

        Args: 
            equation (string): The name of the method to be used to compute
                fitness, as a string. eg, ``'weighted_sum'`` or
                ``'rosenbrock'``.
            parameters (dict): Dictionary of keyword parameter values for the
                method specified in *equation*.

        Returns:
            FitnessFunction callable object
        """

        self.equation = getattr(self, equation)
        self.parameters = parameters  # dictionary

    def weighted_sum(self, truss, parameters):
        """Computes fitness score using a weighted sum of parameters.

        Args:
            truss (Truss object): truss to be scored. Must have mass
                fos attributes defined (for example, by using evaluator).
            parameters (dict): Dictionary with the following entries:

                - ``'goal_fos'`` *(float >= 0)*: Desired factor of safety. Trusses with
                  a smaller fos will be penalized according to *'w_fos'*.
                - ``'critical_nodes'`` *(int, array)*: Array of nodes #s for which 
                  deflection should be minimized. If empty, defaults to all.
                - ``'w_fos'`` *(float >= 0)*: Penalty weight for low fos. Only applied
                  if truss.fos < *'goal_fos'*.
                - ``'w_mass'`` *(float >= 0)*: Penalty applied to mass. Relative
                  magnitude of *'w_mass'* and *'w_fos'* determines importance of
                  minimizing mass vs maximizing fos.
                - ``'w_deflection'`` *(float >=0, array)*: Penalty applied to deflections.
                  If scalar, applies the same penalty to all critical nodes.
                  Can also be an array the same size as *'critical_nodes'* in 
                  which case different penalties will be applied to each node.

        Returns:
            float: Fitness score. Computed as:
            :math:`f = w_{m} m + w_{fos}\max{(\mathrm{fos}_{goal}-\mathrm{fos}_{min}, 0)} 
            + w_{def} ||\mathrm{deflections}||_2`

            :math:`m` is the mass of the stucture, :math:`\mathrm{fos}_{min}` is the 
            lowest fos for the structure under all load conditions.
            If :math:`\mathrm{fos}_{min} > \mathrm{fos}_{goal}`, no fos penalty is applied, so f 
            depends only on mass and deflections.

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
        """Sum of squares of node array elements. aka, sphere function.

        Global min at x = 0 where f = 0.
        This method is primarily supplied for testing of the genetic algorithm,
        and should not be used for structural design.

        Args: 
            truss (Truss object): only uses truss object as container for 
                nodes. No other attributes needed.
            parameters (dict): None needed for this method.

        Returns:
            float: Fitness score. Computed as
            :math:`f(x) = \Sigma_{i=1}^n x_i^2`

            :math:`n` is determined from size of nodes array,
            :math:`x_i` are entries of node array.
        """

        x = truss.rand_nodes.flatten()
        f = np.sum(x**2)
        return f

    def rosenbrock(self, truss, parameters=None):
        """n-dimensional Rosenbrock function.

        Sum of n/2 2D Rosenbrock functions.
        Global min at x=1 where f=0.
        This method is primarily supplied for testing of the genetic algorithm,
        and should not be used for structural design.

        Args: 
            truss (Truss object): only uses truss object as container for 
                nodes. No other attributes needed.
            parameters (dict): None needed for this method.

        Returns:
            float: Fitness score. Computed as
            :math:`f(x) = \Sigma_{i=1}^{n/2}(100*(x_{2i-1}^2 - x_{2i}^2)^2 + (x_{2i-1} - 1)^2)`

            :math:`n` is determined from size of nodes array,
            :math:`x_i` are entries of node array.
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
        """n-dimensional Restrigin function.

        Global min at x=0 where f=0.
        This method is primarily supplied for testing of the genetic algorithm,
        and should not be used for structural design.

        Args: 
            truss (Truss object): only uses truss object as container for 
                nodes. No other attributes needed.
            parameters (dict): None needed for this method.

        Returns:
            float: fitness score. Computed as
            :math:`f(x) = 10n + \Sigma_{i=1}^n (x_i^2 -10\cos{(2 \pi x_i)})`

            :math:`n` is determined from size of nodes array,
            :math:`x_i` are entries of node array.
        """

        A = 10  # normalizing parameters
        x = truss.rand_nodes.flatten()
        n = x.size
        x2 = x**2
        cosx = np.cos(2*np.pi*x)
        f = A*n + np.sum(x2-A*cosx)
        return f

    def __call__(self, truss):
        """Computes fitness score and stores it in truss object.

        Used when a FitnessFunction object has been created with the
        method to be used and any necessary parameters.

        Args:
            truss (Truss object): truss to be scored. 

        Returns:
           None

        """

        f = self.equation(truss, self.parameters)
        truss.fitness_score = f
