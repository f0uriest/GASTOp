"""truss.py
This file is a part of GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements the Truss class.

"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Truss():
    """Implements the Truss object, which is the fundamental object/data
    type in GASTOp.

    Each truss is defined by a collection of nodes (points in x,y,z space),
    edges (connections between nodes), and properties (material and geometric
    properties of the connections between nodes).

    A truss can also have assigned attributes such as factor of safety,
    deflections, mass, cost, or fitness score. These attributes are calculated
    based on the nodes, edges, and properties.
    """

    def __init__(self, user_spec_nodes, rand_nodes, edges,
                 properties, fos=None, deflection=None, mass=None,
                 interference=None, cost=None, num_joints=None,
                 fitness_score=None):
        """Creates a Truss object

        Args:
            user_spec_nodes (ndarray): Array of user specified nodes, such as
                where loads are applied or where the structure is supported.
                Array shape should be nx3, where n is the number of specified
                nodes. Each row should contain the x,y,z coordinates of a node.
            rand_nodes (ndarray): Randomly generated nodes. No loads or supports
                should be assigned to random nodes, as their position may change.
                Array shape should be mx3 where m is the number of random
                nodes. Each row should contain the x,y,z coordinates of a node.
            edges (ndarray): Array of connections between nodes. Array shape
                should be kx2, where k is the number of connections or beams
                in the structure. Each row should be 2 integers, the first being
                number of the starting node and the second being the ending node.
                A value of -1 indicates no connection, and will be ignored.
            properties (ndarray): Array of indices for beam properties. Array
                shape should be a 1d array of length k, where k is the number of
                connections or beams in the structure. Each entry should be an
                integer index into the properties dictionary, with values
                between [0, number of beam types].
            fos (ndarray): Array of factor of safety values. Default None.
            deflection (ndarray): Array of node deflections under load,
                in meters. Default None.
            mass (float): Mass of the structure, in kilograms. Default None.
            interference (float): Total length of members passing through
                user specified areas. Default None.
            cost (float): Cost of the structure in dollars. Default None.
            num_joints (int): Number of connections between members. Default None.
            fitness_score (float): Fitness score of the truss. Default None.

        Returns:
            Truss object.
        """
        self.user_spec_nodes = user_spec_nodes
        self.rand_nodes = rand_nodes
        self.edges = edges
        self.properties = properties
        self.fos = fos
        self.deflection = deflection
        self.mass = mass
        self.interference = interference
        self.cost = cost
        self.num_joints = num_joints
        self.fitness_score = fitness_score

    # def sort(self):
    #     """Not implemented yet.

    #     TODO: method to sort or hash truss object so that two trusses can be
    #     meaningfully compared.
    #     """
    #     pass

    def mark_duplicates(self):
        """Checks truss for duplicate edges or self connected nodes and marks them.

        Any edge that connects a node to itself, or any duplicate edges are
        changed to -1.
        """

        orig_num_edges = self.edges.shape[0]

        # mark self connected edges
        self.edges[self.edges[:, 0] == self.edges[:, 1]] = -1

        # mark duplicate edges
        self.edges.sort()
        unique, idx = np.unique(self.edges, axis=0, return_index=True)
        duplicates = np.setdiff1d(range(orig_num_edges), idx)
        self.edges[duplicates, :] = -1
        return

    def cleaned_params(self):
        """Returns cleaned copies of node, edge, and property arrays.

        Args:
            None

        Returns:
            3-element tuple containing:

            -**nodes** *(ndarray)*: Concatenation of user_spec_nodes and rand_nodes.
            -**edges** *(ndarray)*: Edges array after removing rows with -1 values.
            -**properties** *(ndarray)*: Properties corresponding to remaining edges.

        """
        # make local copies of arrays in case something breaks
        nodes = np.concatenate((self.user_spec_nodes, self.rand_nodes))
        edges = self.edges.copy()
        properties = self.properties.copy()

        # remove self connected edges and duplicate members
        properties = properties[(edges[:, 0]) >= 0]
        edges = edges[(edges[:, 0]) >= 0]
        properties = properties[(edges[:, 1]) >= 0]
        edges = edges[(edges[:, 1]) >= 0]

        return nodes, edges.astype(int), properties.astype(int)

    def __str__(self):
        """Prints the truss to the terminal as a formatted array.

        Prints node numbers and locations, edge numbers and connections, and
        beam material property ID's

        If deflections, mass, fos, or cost are defined, they will be printed as well.

        Args:
            None

        Returns:
            None
        """

        nodes, con, matl = self.cleaned_params()

        s = '\n'
        if self.deflection is not None:
            s += '                Nodes                           Deflections              \n'
            s += '   #       x       y       z            dx           dy           dz      \n'
            for i, line in enumerate(np.concatenate((nodes, self.deflection[:, :3, 0]), axis=1)):
                s += ' {:>3d}    {: .2f}   {: .2f}   {: .2f}       {: .3e}   {: .3e}   {: .3e} \n'.format(
                    i, line[0], line[1], line[2], line[3], line[4], line[5])
        else:
            s += '                Nodes                           Deflections          \n'
            s += '   #       x       y       z            dx           dy           dz       \n'
            for i, line in enumerate(nodes):
                s += ' {:>3d}    {: .2f}   {: .2f}   {: .2f}                    Undefined \n'.format(
                    i, line[0], line[1], line[2])

        s += '\n'
        if self.fos is not None:
            s += '                    Edges  \n'
            s += '        Start    End    Property \n'
            s += '   #    Node     Node     Type       FoS \n'
            for i, line in enumerate(np.concatenate((con, matl.reshape(matl.shape[0], 1), self.fos), axis=1)):
                s += ' {:>3d}    {:>3d}     {:>3d}      {:>3d}       {:>7.2f} \n'.format(
                    i, line[0].astype(int), line[1].astype(int), line[2].astype(int), line[3])
        else:
            s += '                    Edges     \n'
            s += '        Start    End    Property      \n'
            s += '   #    Node     Node     Type       FoS    \n'
            for i, line in enumerate(np.concatenate((con, matl.reshape(matl.shape[0], 1)), axis=1)):
                s += ' {:>3d}    {:>3d}     {:>3d}       {:>3d}      Undefined      \n'.format(
                    i, line[0].astype(int), line[1].astype(int), line[2].astype(int))

        s += '\n'
        if self.mass is not None:
            s += 'Mass: {:.3f} kg \n'.format(self.mass)
        else:
            s += 'Mass: Undefined \n'

        if self.cost is not None:
            s += 'Cost: $ {:.2f} \n '.format(self.cost)
        else:
            s += 'Cost: Undefined \n'
        return s

    def plot(self, domain=None, loads=None, fixtures=None,
             deflection=False, load_scale=None, def_scale=100, ax=None, fig=None,setup_only = False):
        """Plots a truss object as a 3D wireframe

        Args:
            self (Truss object): truss to be plotted. Must have user_spec_nodes,
                rand_nodes, edges defined.
            domain (ndarray): (optional) axis limits in x,y,z, specified as a
                3x2 array: [[xmin, xmax],[ymin,ymax],[zmin,zmax]].
            loads (ndarray): (optional) Array of loads to be plotted as arrows.
                Specified as nx6 array, each row corresponding to the load at
                the node matching the row #. Load format:
                [Fx,Fy,Fz,Mx,My,Mz]
            fixtures (ndarray): (optional) Array of fixtures to be plotted as blobs.
                Specified as an nx6 array, each row corresponding to fixtures at
                the node matching the row #. Format:
                [Dx,Dy,Dz,Rx,Ry,Rz] value of 1 means fixed in that direction,
                value of zero is free.
            deflection (bool): If True, deflections will be plotted superposed on
                the undeformed structure. Relative size of deflections is governed
                by *def_scale*.
            load_scale (float): Size load vector arrows should be scaled by.
            def_scale (float): Scaling for deflections. *def_scale*=1
                means actual size, larger than 1 magnifies.

        Returns:
            None
        """

        nodes, con, matl = self.cleaned_params()

        num_con = con.shape[0]

        size_scale = (nodes.max(axis=0)-nodes.min(axis=0)).max()

        edge_vec_start = nodes[con[:, 0], :]  # sfr
        edge_vec_end = nodes[con[:, 1], :]  # sfr

        if load_scale is None and loads is not None:
            load_scale = size_scale/np.abs(loads).max()/5

        if ax is None:
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            prog = 0
            ax.set_title('Truss')
        else:
            prog = 1  # currently in progress monitor
            ax.set_title('Truss Evolution')

        ax.set_xlabel('X [m]', fontsize=14, labelpad=10)
        ax.set_ylabel('Y [m]', fontsize=14, labelpad=10)
        ax.set_zlabel('Z [m]', fontsize=14, labelpad=10)
        ax.tick_params(labelsize='small')
        ax.view_init(30, -45)

        if domain is not None:
            ax.set_xlim(domain[:, 0])
            ax.set_ylim(domain[:, 1])
            ax.set_zlim(domain[:, 2])

        if not setup_only:
            for i in range(num_con):
                ax.plot([edge_vec_start[i, 0], edge_vec_end[i, 0]],
                        [edge_vec_start[i, 1], edge_vec_end[i, 1]],
                        [edge_vec_start[i, 2], edge_vec_end[i, 2]], 'k-')

        if deflection and not setup_only:
            def_nodes = nodes + def_scale*self.deflection[:, :3, 0]
            def_edge_vec_start = def_nodes[con[:, 0], :]
            def_edge_vec_end = def_nodes[con[:, 1], :]
            for i in range(num_con):
                ax.plot([def_edge_vec_start[i, 0], def_edge_vec_end[i, 0]],
                        [def_edge_vec_start[i, 1], def_edge_vec_end[i, 1]],
                        [def_edge_vec_start[i, 2], def_edge_vec_end[i, 2]], 'b-',alpha=0.5)#,label='Displaced Truss')

        if loads is not None:
            ax.quiver(nodes[:, 0], nodes[:, 1], nodes[:, 2],
                      loads[:, 0, 0], loads[:, 1, 0], loads[:, 2, 0],
                      length=load_scale, pivot='tip', color='r')
            load_nodes = nodes[loads[:, :, 0].any(axis=1)]
            ax.scatter(load_nodes[:, 0], load_nodes[:, 1], load_nodes[:, 2],
                       color='red', marker='o', depthshade=False, s=100)

        if fixtures is not None:
            fix_nodes = nodes[fixtures[:, :, 0].any(axis=1)]
            ax.scatter(fix_nodes[:, 0], fix_nodes[:, 1], fix_nodes[:, 2],
                       color='green', marker='o', depthshade=False, s=100)
        if prog == 0:  # only shows it if not being called within ProgMon
            plt.show()
            plt.gcf().savefig('final_result.png')
