import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import timeit

setup = '''
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import timeit

from __main__ import plot3D, progress_monitor

domain2 = np.array([[-1,5], [-1,1], [-1,2]])
fitscore = np.random.rand(1000)
fitscore.sort()

nodes = np.array( [[0.00 ,  -0.50 ,   0.00],
     [0.00 ,   0.50   , 0.00],
     [0.00  ,  0.00   , 1.00],
     [2.00  ,  0.00   , 0.00],
      [1.71 ,  -0.87  , -0.29],
   [-0.51  , -0.11   ,-0.32],
    [3.19  , -0.73   ,-0.10],
   [-0.12  , -0.23   , 0.72],
   [-0.49  , -0.78  , -0.28],
   [-0.82  ,  0.26  , -0.71],
    [4.66  ,  0.30 ,   1.32],
  [2.09    ,0.01  ,  0.83  ],
    [3.20  , -0.75  ,  0.08],
    [0.43  ,  0.59 ,   1.32]])
con = np.array([[0   ,    3],
       [1   ,    3 ],
        [1   ,    9],
         [2   ,   11],
        [2     , 13],
         [3     , 13],
         [8    ,  13]])
'''


domain2 = np.array([[-1,5], [-1,1], [-1,2]])


fitscore = np.random.rand(1000)
fitscore.sort()

nodes = np.array( [[0.00 ,  -0.50 ,   0.00],
     [0.00 ,   0.50   , 0.00],
     [0.00  ,  0.00   , 1.00],
     [2.00  ,  0.00   , 0.00],
      [1.71 ,  -0.87  , -0.29],
   [-0.51  , -0.11   ,-0.32],
    [3.19  , -0.73   ,-0.10],
   [-0.12  , -0.23   , 0.72],
   [-0.49  , -0.78  , -0.28],
   [-0.82  ,  0.26  , -0.71],
    [4.66  ,  0.30 ,   1.32],
  [2.09    ,0.01  ,  0.83  ],
    [3.20  , -0.75  ,  0.08],
    [0.43  ,  0.59 ,   1.32]])
con = np.array([[0   ,    3],
       [1   ,    3 ],
        [1   ,    9],
         [2   ,   11],
        [2     , 13],
         [3     , 13],
         [8    ,  13]])


def plot3D(domain=None, loads=None, fixtures=None,
         deflection=False, load_scale=None, def_scale=100, ax=None, fig=None):

    #nodes, con, matl = self.cleaned_params()

    num_con = con.shape[0]

    size_scale = (nodes.max(axis=0)-nodes.min(axis=0)).max()

    edge_vec_start = nodes[con[:, 0], :] #sfr
    edge_vec_end = nodes[con[:, 1], :] #sfr



    if load_scale is None and loads is not None:
        load_scale = size_scale/np.abs(loads).max()/5

    if ax is None:
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        prog = 0
        ax.set_title('Truss')
    else:
        prog = 1 # currently in progress monitor
        ax.set_title('Truss Evolution')

    ax.set_xlabel('X [m]',fontsize=14,labelpad=10)
    ax.set_ylabel('Y [m]',fontsize=14,labelpad=10)
    ax.set_zlabel('Z [m]',fontsize=14,labelpad=10)
    ax.tick_params(labelsize = 'small')

    if domain is not None:
        ax.set_xlim(domain[0, :])
        ax.set_ylim(domain[1, :])
        ax.set_zlim(domain[2, :])

    if deflection:
        def_nodes = nodes + def_scale*self.deflection[:, :3, 0]
        def_edge_vec_start = def_nodes[con[:, 0], :]
        def_edge_vec_end = def_nodes[con[:, 1], :]
        for i in range(num_con):
            ax.plot([def_edge_vec_start[i, 0], def_edge_vec_end[i, 0]],
                    [def_edge_vec_start[i, 1], def_edge_vec_end[i, 1]],
                    [def_edge_vec_start[i, 2], def_edge_vec_end[i, 2]], 'b-')

    #edge_vec_start = nodes[con[:, 0], :] #sfr
    #edge_vec_end = nodes[con[:, 1], :] #sfr

    # ****
    for i in range(num_con):
        ax.plot([edge_vec_start[i, 0], edge_vec_end[i, 0]],
                [edge_vec_start[i, 1], edge_vec_end[i, 1]],
                [edge_vec_start[i, 2], edge_vec_end[i, 2]], 'k-')

    if loads is not None:
        ax.quiver(nodes[:, 0], nodes[:, 1], nodes[:, 2],
                  loads[:, 0, 0], loads[:, 1, 0], loads[:, 2, 0],
                  length=load_scale, pivot='tip', color='r')

    if fixtures is not None:
        fix_nodes = nodes[fixtures[:, :, 0].any(axis=1)]
        ax.scatter(fix_nodes[:, 0], fix_nodes[:, 1], fix_nodes[:, 2],
                   c='g', marker='o', depthshade=False, s=100)
    if prog == 0: #only shows it if not being called within ProgMon
        plt.show()


def progress_monitor(current_gen, fitscore,progress_display):

    # three options: plot, progress bar ish thing, no output just append
    # calc population diversity and plot stuff or show current results
    #fitscore = [i.fitness_score for i in population] #extract factor of safety from each truss object in population
    fitscore_min = fitscore[0]

    if progress_display == 2:

        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1) #does this need self.?
        plt.xlim(0, 5)
        plt.ylabel('Minimum Fitness Score')
        plt.xlabel('Iteration')

        if current_gen==0:
            pop_start = fitscore_min # store initial min fitscore (should be worst)

        ax1.scatter(current_gen,fitscore_min,c=[1,0,0])
        # set text with current min fitscore
        plot_text=ax1.text(1, 1, round(fitscore_min,3),bbox=dict(facecolor='white', alpha=1))
        # set box to same size
        plot_text._bbox_patch._mutation_aspect = 0.1
        plot_text.get_bbox_patch().set_boxstyle("square", pad=1)

        #self.ax1.scatter(current_gen,np.amin(fitscore),c=[0,0,0]) #plot minimum fitscore for current gen in black
        plt.pause(0.001) #pause for 0.001s to allow plot to update, can potentially remove this

    elif progress_display == 3:

        fig = plt.figure()
        #self.ax3 = self.fig.add_subplot(1,1,1)#self.fig.gca(projection='3d')
        ax3 = fig.gca(projection='3d')

        #population.sort(key=lambda x: x.fitness_score)

        #best_truss = population[0]
        ax3.cla()
        #edge_vec_start, edge_vec_end, num_con = best_truss.plot(ax=self.ax3,fig = self.fig)
        plot3D(domain=domain2,ax=ax3,fig = fig)

        plot_text=ax3.text(domain2[0][1]-1.0,domain2[1][1]-1.0,domain2[2][1],"Iteration: " + str(current_gen),bbox=dict(facecolor='white', alpha=1))
        # # set box to same size
        plot_text._bbox_patch._mutation_aspect = 0.1
        plot_text.get_bbox_patch().set_boxstyle("square", pad=1)

        plt.pause(0.001)


#plot3D(domain=domain2)
progress_monitor(3, fitscore, 3)

ntests = 50

test2D = '''progress_monitor(3, fitscore, 2)'''
test3D = '''progress_monitor(3, fitscore, 3)'''

time2D = timeit.timeit(setup=setup,stmt=test2D,number=ntests)
time3D = timeit.timeit(setup=setup,stmt=test3D,number=ntests)

print('method2D: ' + str(time2D))
print('method3D: ' + str(time3D))


# n = 30:
#method2D: 4.366851215003408
#method3D: 6.209585124001023

#n=50
#method2D: 7.711342558002798
#method3D: 13.652633436999167
