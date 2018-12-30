
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

##plt.ion() #look into multithreading this
style.use('fivethirtyeight')

class ProgMon():

    def __init__(self,progress_display,num_generations):

        self.progress_display = progress_display
        self.pop_progress = []

        if self.progress_display == 2: #check if figure method of progress monitoring is requested
            # initialize plot:
            fig = plt.figure()
            self.ax1 = fig.add_subplot(1,1,1) #does this need self.?
            plt.xlim(0, num_generations)
            plt.ylabel('fitscore')
            plt.xlabel('iteration')
            plt.xlim(0,num_generations)
        #



    def progress_monitor(self,current_gen,population):

        # three options: plot, progress bar ish thing, no output just append
        # calc population diversity and plot stuff or show current results
        fitscore = [i.fitness_score for i in population] #extract factor of safety from each truss object in population
        self.pop_progress.append(population) #append to history
        if self.progress_display == 1:
            print(current_gen,np.amin(fitscore))
        elif self.progress_display == 2:
            #print(current_gen,min(fitscore))
            self.ax1.scatter(current_gen,np.amin(fitscore),c=[0,0,0]) #plot minimum fitscore for current gen in black
            plt.pause(0.0001) #pause for 0.0001s to allow plot to update, can potentially remove this
