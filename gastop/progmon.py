import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

##plt.ion() #look into multithreading this
style.use('fivethirtyeight')


class ProgMon():

    def __init__(self,progress_display,num_generations):

        self.progress_display = progress_display
        self.num_gens = num_generations
        self.orderofgen = int(np.log10(self.num_gens))*10
        self.pop_progress = []
        self.pop_start = []

        if self.progress_display == 2:  # check if figure method of progress monitoring is requested
            # initialize plot:
            fig = plt.figure()
            self.ax1 = fig.add_subplot(1,1,1) #does this need self.?
            plt.xlim(0, self.num_gens)
            plt.ylabel('Minimum Fitness Score')
            plt.xlabel('Iteration')
        elif self.progress_display == 3:
            self.fig = plt.figure()
            #self.ax3 = self.fig.add_subplot(1,1,1)#self.fig.gca(projection='3d')
            self.ax3 = self.fig.gca(projection='3d')
            #plt.ylabel('Y [m]')
            #plt.xlabel('X [m]')
            #plt.zlabel('Z [m]')

            #plt.yscale('log')
            #
            # self.ax2 = fig.add_subplot(1,2,2) #does this need self.?
            # plt.xlim(0, num_generations)
            # plt.ylabel('Min Fitness Score')
            # plt.xlabel('Iteration')
            # plt.xlim(0,num_generations)
        #

    def progress_monitor(self, current_gen, population):

        # three options: plot, progress bar ish thing, no output just append
        # calc population diversity and plot stuff or show current results
        fitscore = [i.fitness_score for i in population] #extract factor of safety from each truss object in population
        fitscore_min = np.amin(fitscore)

        self.pop_progress.append(population) #append to history
        #if self.progress_display == 1:
        #    test = np.amin(fitscore)
        if self.progress_display == 2:
            if current_gen==0:
                self.pop_start = fitscore_min # store initial min fitscore (should be worst)
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
            #self.pop_prop.append(fitscore_range)

            #self.ax1.errorbar(current_gen, fitscore_med, yerr=fitscore_range_scaled, fmt='o',c=[0,0,0])
            #self.ax1.scatter(current_gen,fitscore_med,c=[0,0,0])

            self.ax1.scatter(current_gen,fitscore_min,c=[1,0,0])
            # set text with current min fitscore
            plot_text=self.ax1.text(self.num_gens-self.orderofgen, self.pop_start, round(fitscore_min,3),bbox=dict(facecolor='white', alpha=1))
            # set box to same size
            plot_text._bbox_patch._mutation_aspect = 0.1
            plot_text.get_bbox_patch().set_boxstyle("square", pad=1)

            #self.ax1.scatter(current_gen,np.amin(fitscore),c=[0,0,0]) #plot minimum fitscore for current gen in black
            plt.pause(0.0001) #pause for 0.0001s to allow plot to update, can potentially remove this

        elif self.progress_display == 3: #does not work yet
            population.sort(key=lambda x: x.fitness_score)
            best_truss = population[0]

            edge_vec_start, edge_vec_end, num_con = best_truss.plot(ax=self.ax3,fig = self.fig)

            self.ax3.cla()
            #self.fig.canvas.flush_events()
            for i in range(num_con):
                self.ax3.plot([edge_vec_start[i, 0], edge_vec_end[i, 0]],
                        [edge_vec_start[i, 1], edge_vec_end[i, 1]],
                        [edge_vec_start[i, 2], edge_vec_end[i, 2]], 'k-')
            #iter = "Iteration:" + str(current_gen)
            plot_text=self.ax3.text(1,1,1,"Iteration: " + str(current_gen),bbox=dict(facecolor='white', alpha=1))
            # # set box to same size

            plot_text._bbox_patch._mutation_aspect = 0.1
            plot_text.get_bbox_patch().set_boxstyle("square", pad=1)


            plt.pause(0.0001)
            #self.ax3.draw()
            #self.fig.canvas.draw()
            #self.fig.canvas.flush_events()
