
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

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
    y = 0
    style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    plt.ylabel('convergence')
    plt.xlabel('iteration')


    for i in range(n):

        y = 2.0*i
        progress(i,y,ax1)
        print(y)
    plt.show()

    return y


def progress(i,y,ax1):
#    if i==1:
        #style.use('fivethirtyeight')
        #fig = plt.figure()
        #ax1 = fig.add_subplot(1,1,1)
        #plt.ylabel('convergence')
        #plt.xlabel('iteration')
#    else:
    ax1.scatter(i,y,c=[0,0,0])
    plt.pause(0.0001) #time it waits for plot to update


y = counter(10)
