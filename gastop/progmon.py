"""progmon.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the ProgMon class.

"""

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from matplotlib.animation import FuncAnimation
import collections

# plt.ion() #look into multithreading this
style.use('fivethirtyeight')


class ProgMon():
    """Plots fitness score or truss evolution and stores population statistics.

    The GenAlg Class orchestrates all of the other functions that perform
    functions to change the population and its elements. In this case, such
    classes are crossover, evaluator, encoders, fitness, mutator, selector, and
    truss.

    In brief, GenAlg calls many other functions in order to create a generation
    which is then analyzed to fully determine its relavant properties. These
    properties are then used to create a new generation and the process repeats
    until a final solution is reached.

    """

    def __init__(self, progress_fitness, progress_truss, num_generations, domain=None, loads=None, fixtures=None):
        """Creates a ProgMon object

        Once created, the object will store all of the relavant information
        about a population. The object also contains the necessary functions to
        modify itself, evaluate its 'goodness', and then create new members for
        the next generation.

        Args:
            Either:
            config (dict): Configuration dictionary with parameters, such as one
                created by :meth:`gastop.utilities.init_file_parser`
            config (str): File path to config file to be parsed. Used
                instead of passing config dictionary directly.

        Returns:
            GenAlg callable object
        """

        self.progress_fitness = progress_fitness
        self.progress_truss = progress_truss
        self.num_gens = num_generations
        # is this doing what i want it to
        self.orderofgen = 10**(int(np.log10(self.num_gens)))
        self.pop_progress = collections.defaultdict(dict)
        self.dict_headings = ['Generation','Best Truss','Best Fitness Score','Population Median Fitness Score','Population Fitness Score Range']

        self.pop_start = []
        self.domain = domain
        self.loads = loads
        self.fixtures = fixtures


        if self.progress_fitness and self.progress_truss:
            self.fig = plt.figure()
            self.ax1 = self.fig.add_subplot(1, 2, 1)
            self.ax1.set_title('Fitness Score Evolution')
            plt.xlim(0, self.num_gens)
            plt.ylabel('Minimum Fitness Score')
            plt.xlabel('Iteration')
            self.ax3 = self.fig.add_subplot(122, projection='3d')

        elif self.progress_fitness:  # check if figure method of progress monitoring is requested
            # initialize plot:
            fig = plt.figure()
            self.ax1 = fig.add_subplot(1, 1, 1)  # does this need self.?
            plt.xlim(0, self.num_gens)
            plt.ylabel('Minimum Fitness Score')
            plt.xlabel('Iteration')
            self.ax1.set_title('Fitness Score Evolution')

        elif self.progress_truss:
            self.fig = plt.figure()
            # self.ax3 = self.fig.add_subplot(1,1,1)#self.fig.gca(projection='3d')
            self.ax3 = self.fig.gca(projection='3d')

    def progress_monitor(self, current_gen, population):

        # three options: plot, progress bar ish thing, no output just append
        # calc population diversity and plot stuff or show current results
        # extract factor of safety from each truss object in population
        fitscore = [i.fitness_score for i in population]
        fitscore_min = fitscore[0]
        fitscore_median = np.median(fitscore)
        fitscore_range = fitscore[-1] - fitscore_min

        pop_stats = [current_gen,population[0],fitscore_min,fitscore_median,fitscore_range]

        #More readable but dumb?
        #self.pop_progress['Generation '+str(current_gen)]['Generation'] = current_gen
        #self.pop_progress['Generation '+str(current_gen)]['Best Truss'] = population[0]
        #self.pop_progress['Generation '+str(current_gen)]['Best Fitness Score'] = fitscore_min
        #self.pop_progress['Generation '+str(current_gen)]['Population Median Fitness Score'] = fitscore_median
        #self.pop_progress['Generation '+str(current_gen)]['Population Fitness Score Range'] = fitscore_range

        for j in range(5):
            self.pop_progress['Generation '+str(current_gen)][self.dict_headings[j]] = pop_stats[j]
        #self.pop_progress.append([current_gen,population[0],fitscore_min,fitscore_median,fitscore_range])


        if current_gen == 0:
            # store initial min fitscore (should be worst) for plotting box
            self.pop_start = fitscore_min

        if self.progress_fitness and self.progress_truss:


            # ** Fitness score plot
            self.ax1.scatter(current_gen+1.0, fitscore_min,
                             c=[[1, 0, 0]])  # change c to be 2D array?
            # set text with current min fitscore
            plot_text = self.ax1.text(self.num_gens-self.orderofgen, self.pop_start, round(
                fitscore_min, 3), bbox=dict(facecolor='white', alpha=1))
            # set box to same size
            plot_text._bbox_patch._mutation_aspect = 0.1
            plot_text.get_bbox_patch().set_boxstyle("square", pad=1)

            # ** Truss plot
            best_truss = population[0]
            self.ax3.cla()
            #edge_vec_start, edge_vec_end, num_con = best_truss.plot(ax=self.ax3,fig = self.fig)
            best_truss.plot(domain=self.domain,
                            fixtures=self.fixtures, ax=self.ax3, fig=self.fig)

            plot_text3d = self.ax3.text(self.domain[1][0]-1.0, self.domain[1][1]-1.0, self.domain[1]
                                        [2], "Iteration: " + str(current_gen), bbox=dict(facecolor='white', alpha=1))
            # # set box to same size
            plot_text3d._bbox_patch._mutation_aspect = 0.1
            plot_text3d.get_bbox_patch().set_boxstyle("square", pad=1)

            # pause for 0.001s to allow plot to update, can potentially remove this
            plt.pause(0.001)

        elif self.progress_fitness:

            #     fitscore_range_scaled = 1.0
            #     #self.pop_prop(current_gen) = (np.amax(fitscore) - np.amin(fitscore))/2.0
            #     self.pop_prop.append([(np.amax(fitscore) - np.amin(fitscore))/2.0])
            # else:
            #     fitscore_range = (np.amax(fitscore) - np.amin(fitscore))/2.0
            #     fitscore_range_scaled = fitscore_range/self.pop_prop[current_gen-1]
            #     self.pop_prop.append([fitscore_range])
            #     #self.pop_prop(current_gen) = fitscore_range
            #
            # fitscore_med = np.median(fitscore)
            # self.pop_prop.append(fitscore_range)

            #self.ax1.errorbar(current_gen, fitscore_med, yerr=fitscore_range_scaled, fmt='o',c=[0,0,0])
            # self.ax1.scatter(current_gen,fitscore_med,c=[0,0,0])

            self.ax1.scatter(current_gen + 1.0, fitscore_min,
                             c=[[1, 0, 0]])  # change c to be 2D array?
            # set text with current min fitscore
            plot_text = self.ax1.text(self.num_gens-self.orderofgen, self.pop_start, round(
                fitscore_min, 3), bbox=dict(facecolor='white', alpha=1))
            # set box to same size
            plot_text._bbox_patch._mutation_aspect = 0.1
            plot_text.get_bbox_patch().set_boxstyle("square", pad=1)

            # self.ax1.scatter(current_gen,np.amin(fitscore),c=[0,0,0]) #plot minimum fitscore for current gen in black
            # pause for 0.001s to allow plot to update, can potentially remove this
            plt.pause(0.001)

        elif self.progress_truss:
            #population.sort(key=lambda x: x.fitness_score)

            best_truss = population[0]
            self.ax3.cla()
            #edge_vec_start, edge_vec_end, num_con = best_truss.plot(ax=self.ax3,fig = self.fig)
            best_truss.plot(domain=self.domain,
                            fixtures=self.fixtures, ax=self.ax3, fig=self.fig)

            plot_text = self.ax3.text(self.domain[1][0]-1.0, self.domain[1][1]-1.0, self.domain[1]
                                      [2], "Iteration: " + str(current_gen), bbox=dict(facecolor='white', alpha=1))
            # # set box to same size
            plot_text._bbox_patch._mutation_aspect = 0.1
            plot_text.get_bbox_patch().set_boxstyle("square", pad=1)

            plt.pause(0.001)
            self.fig.savefig('animation/truss_evo_iter' +
                             str(current_gen) + '.png')
