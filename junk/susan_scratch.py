
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
from tqdm import tqdm
import numpy as np
import collections
from matplotlib.path import Path
from matplotlib.patches import BoxStyle
import matplotlib.textpath as textpath
from matplotlib.artist import Artist

from matplotlib.offsetbox import AnchoredText

##plt.ion() #look into multithreading this
#style.use('fivethirtyeight')
#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
#plt.ylabel('convergence')
#plt.xlabel('iteration')

        # if self.progress_fitness and self.progress_truss:
        #
        #
        #     # Fitness score plot
        #     self.ax1.scatter(current_gen+1.0, fitscore_min,c=[[0, 0, 0]])  # change c to be 2D array?
        #
        #     [txt.set_visible(False) for txt in self.ax1.texts]  #clear old text box
        #     self.ax1.text(self.num_gens, self.pop_start, round(
        #         fitscore_min, 3), bbox=dict(facecolor='white', alpha=1),horizontalalignment='right')
        #
        #     # Truss plot
        #     self.ax3.cla()
        #     best_truss.plot(domain=self.domain, loads = self.loads,
        #                     fixtures=self.fixtures, ax=self.ax3, fig=self.fig)
        #
        #     self.ax3.text(self.domain[1][0]-1.0, self.domain[1][1]-1.0, self.domain[1][2],
        #     "Iteration: " + str(current_gen+1.0), bbox=dict(facecolor='white', alpha=1))
        #
        #     plt.pause(0.001)

def run(self):
    y = counter(10)
    print(y)

def counter(n):
    y0 = np.array([1,2,3])
    style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(1,2,1)
    plt.ylabel('convergence')
    plt.xlabel('iteration')
    plt.xlim(0,n)

    ax2 = fig.add_subplot(1,2,2)
    plt.ylabel('test')
    plt.xlabel('iteration')
    #plt.yscale('log')
    #plt.text(2,4,"0")
    plt.xlim(0,2)
    #plt.ylim(0,12)
    test  = []

    d = collections.defaultdict(dict)



    for i in tqdm(range(n)):
        y = 10.0-i*y0
        #for j in range(3):
        #    d['Iteration '+str(i)]['y'+str(j)] = y[j]
        d['Iteration'+str(i)]['y0'] = y[0]
        d['Iteration'+str(i)]['y1'] = y[1]
        d['Iteration'+str(i)]['y012'] = y
        if i == 0:
            test = np.min(y)
        # else:
        #     test.append(test[i-1])
        #fig.clf()
        progress(i,y,ax1,ax2,n,test,fig)
        print(np.min(y))
    plt.show()

    return y, d


def progress(i,y,ax1,ax2,n,test,fig):
#    if i==1:
        #style.use('fivethirtyeight')
        #fig = plt.figure()
        #ax1 = fig.add_subplot(1,1,1)
        #plt.ylabel('convergence')
        #plt.xlabel('iteration')
#    else:
    err_range = (np.amax(y) - np.amin(y))/2.0


    #ax2.cla()
    ax1.errorbar(i, np.mean(y), yerr=err_range, fmt='o')
    if i!=0:
        #Artist.remove(ax1.texts)
        #fig.text.remove()
        #print(ax1.get_extents)
        [Artist.remove(txt) for txt in ax1.texts]
    [txt.set_visible(False) for txt in ax1.texts]
    #if i != 0:
    #    textvar = ax1.texts
        #textvar.remove(True)
        #ax1.remove(textvar)
        #ax1.texts.set_visible(False)
    #    [txt.set_visible(False) for txt in ax1.texts]
        #for txt in ax1.texts:
            #txt.set_visible(False)

    text_box = AnchoredText(np.amin(y), frameon=True, loc=1, pad=0.5)
    plt.setp(text_box.patch, facecolor='white', alpha=1)
    ax1.add_artist(text_box)

    #plot_text = ax1.text(3, 9, np.amin(y),bbox=dict(facecolor='white', alpha=1))
    #plot_text._bbox_patch._mutation_aspect = 0.1
    #plot_text.get_bbox_patch().set_boxstyle("square", pad=1)


    #ax2.text(n,4,np.amin(y),bbox=dict(facecolor='white', alpha=1))


    ax2.plot(range(3),y,c=[0,0,0])

    #ax2.xaxis.font(12)
    ax2.tick_params(labelsize = 'small')


    #fig.clf()
    #ax2.draw()


    #ax2.text()
    plt.pause(0.5) #time it waits for plot to update


counter(4)
#print(dict_full)
