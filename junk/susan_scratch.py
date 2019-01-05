
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
from tqdm import tqdm
import numpy as np
import collections


##plt.ion() #look into multithreading this
#style.use('fivethirtyeight')
#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
#plt.ylabel('convergence')
#plt.xlabel('iteration')

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


    ax2.cla()
    ax1.errorbar(i, np.mean(y), yerr=err_range, fmt='o')
    #ax2.text(n,4,np.amin(y),bbox=dict(facecolor='white', alpha=1))

    ax2.text(n-1, test-1, np.amin(y),
        bbox=dict(facecolor='white', alpha=1))
    ax2.plot(range(3),y,c=[0,0,0])
    #ax2.xaxis.font(12)
    ax2.tick_params(labelsize = 'small')


    #fig.clf()
    #ax2.draw()


    #ax2.text()
    plt.pause(0.5) #time it waits for plot to update


y,dict_full = counter(4)
print(dict_full)
