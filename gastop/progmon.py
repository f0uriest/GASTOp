"""progmon.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the ProgMon class.

"""

import matplotlib.pyplot as plt
import numpy as np
import collections



class ProgMon():
    """Plots fitness score or truss evolution and stores population statistics.

    This class takes in the current sorted population and displays information
    based on the user requests.  If truss monitoring is requested it calls the
    plot method.  The population stats are returned via GenAlg and written to a
    json file, allowing the user to plot the evolution after the optimization is
    complete.

    """

    def __init__(self, progress_fitness, progress_truss, num_generations, domain=None, loads=None, fixtures=None):
        """Creates a ProgMon object

        Once created, the object will store all of the relavant information
        about a progess monitor. The figures are also initialized upon
        object instatiation.

        Args:
            progress_fitness (boolean): if true the minimum fitness score of the
                population is plotted each iteration
            progress_truss (boolean): if true the truss corresponding to the
                minimum fitness score is displayed each iteration
            num_generations (integer): indicates the number of generations, used
                when initializing the fitness figure
            domain (numpy array): indicates bounds of design area, used when
                *progress_truss* is true
            loads (numpy array): indicates magnitude and direction of loads
                applied to *user_spec_nodes*, used when *progress_truss* is true
            fixtures (numpy array): indicates fixed DOFs of *user_spec_nodes*,
                used when *progress_truss* is true

        Returns:
            Nothing
        """

        self.progress_fitness = progress_fitness
        self.progress_truss = progress_truss
        self.num_gens = num_generations
        self.pop_progress = collections.defaultdict(dict)

        self.pop_start = []
        self.box_size = []
        self.domain = domain
        self.loads = loads
        self.fixtures = fixtures


        if self.progress_fitness and self.progress_truss:
            self.fig = plt.figure(figsize = [10, 5])
            self.ax1 = self.fig.add_subplot(1, 2, 1)
            self.ax1.set_title('Fitness Score Evolution')
            self.ax1.set_yscale('log')
            plt.xlim(0, self.num_gens+1.0)
            plt.ylabel('Minimum Fitness Score')
            plt.xlabel('Generation')
            self.ax3 = self.fig.add_subplot(122, projection='3d')

        elif self.progress_fitness:

            fig = plt.figure()
            self.ax1 = fig.add_subplot(1, 1, 1)
            plt.xlim(0, self.num_gens+1.0)
            plt.ylabel('Minimum Fitness Score')
            plt.xlabel('Generation')
            self.ax1.set_title('Fitness Score Evolution')
            self.ax1.set_yscale('log')

        elif self.progress_truss:
            self.fig = plt.figure()
            self.ax3 = self.fig.gca(projection='3d')

    def progress_monitor(self, current_gen, population):

        """Updates progress monitor plots

        Function is passed the sorted population and plots either the current
        generation's best fitness score, best truss, or both.  If the truss is
        displayed, the plot method of the truss object is called but passed the
        figure instantiated in the init method.

        Args:
            progress_fitness (boolean): if true the minimum fitness score of the
                population is plotted each iteration
            progress_truss (boolean): if true the truss corresponding to the
                minimum fitness score is displayed each iteration
            num_generations (integer): indicates the number of generations, used
                when initializing the *progress_fitness* figure
            domain (numpy array): indicates bounds of design area, used when
                *progress_truss* is true
            loads (numpy array): indicates magnitude and direction of loads
                applied to *user_spec_nodes*, used when *progress_truss* is true
            fixtures (numpy array): indicates fixed DOFs of *user_spec_nodes*,
                used when *progress_truss* is true

        Returns:
            Nothing
        """
        try:
            fitscore = [i.fitness_score for i in population]
            fitscore_min = fitscore[0]
            fitscore_median = np.median(fitscore)
            fitscore_range = fitscore[-1] - fitscore_min
            best_truss = population[0]
            pop_stats = [current_gen+1,best_truss,fitscore_min,fitscore_median,fitscore_range]
            dict_headings = ['Generation','Best Truss','Best Fitness Score',
            'Population Median Fitness Score','Population Fitness Score Range']

            # Store population stats:
            for j in range(5):
                self.pop_progress['Generation '+str(current_gen+1)][dict_headings[j]] = pop_stats[j]
        except TypeError: # population has no len when called from save_gif
            fitscore = population.fitness_score
            fitscore_min = fitscore
            best_truss = population

        if current_gen == 0:
            # store initial min fitscore (should be worst) for plotting box
            self.pop_start = fitscore_min


        if self.progress_fitness:

            self.ax1.scatter(current_gen+1.0, fitscore_min,
                             c=[[0, 0, 0]])

            [txt.set_visible(False) for txt in self.ax1.texts]
            self.ax1.text(self.num_gens-1.0, self.pop_start, 'Min Fitness Score: ' + str(round(
                fitscore_min, 3)), bbox=dict(facecolor='white', alpha=1),horizontalalignment='right')

            plt.pause(0.001)

        if self.progress_truss:

            self.ax3.cla()
            best_truss.plot(domain=self.domain, loads = self.loads,
                            fixtures=self.fixtures, ax=self.ax3, fig=self.fig)

            self.ax3.text(self.domain[1][0]-1.0, self.domain[1][1]-1.0, self.domain[1]
                                      [2], "Iteration: " + str(current_gen+1.0), bbox=dict(facecolor='white', alpha=1))

        plt.pause(0.001)
