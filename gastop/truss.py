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

        nodes = np.concatenate((self.user_spec_nodes, self.rand_nodes), axis=0)
        con = self.edges.copy()
        matl = self.properties.copy()

        # remove self connected edges and duplicate members
        matl = matl[(con[:, 0]) >= 0]
        con = con[(con[:, 0]) >= 0]
        matl = matl[(con[:, 1]) >= 0]
        con = con[(con[:, 1]) >= 0]

        s = '\n'
        if self.deflection is not None:
            s += '                Nodes                           Deflections              \n'
            s += '   #       x       y       z            dx           dy           dz      \n'
            for i, line in enumerate(np.concatenate((nodes, self.deflection[:, :3, 0]), axis=1)):
                s += f' {i:>3d}    {line[0]: .2f}   {line[1]: .2f}   {line[2]: .2f}       {line[3]: .3e}   {line[4]: .3e}   {line[5]: .3e} \n'
        else:
            s += '                Nodes                           Deflections          \n'
            s += '   #       x       y       z            dx           dy           dz       \n'
            for i, line in enumerate(nodes):
                s += f' {i:>3d}    {line[0]: .2f}   {line[1]: .2f}   {line[2]: .2f}                    Undefined \n'

        s += '\n'
        if self.fos is not None:
            s += '                    Edges  \n'
            s += '        Start    End    Property \n'
            s += '   #    Node     Node     Type       FoS \n'
            for i, line in enumerate(np.concatenate((con, matl.reshape(matl.shape[0], 1), self.fos), axis=1)):
                s += f' {i:>3d}    {line[0].astype(int):>3d}     {line[1].astype(int):>3d}      {line[2].astype(int):>3d}       {line[3]:>7.2f} \n'
        else:
            s += '                    Edges     \n'
            s += '        Start    End    Property      \n'
            s += '   #    Node     Node     Type       FoS    \n'
            for i, line in enumerate(np.concatenate((con, matl.reshape(matl.shape[0], 1)), axis=1)):
                s += f' {i:>3d}    {line[0].astype(int):>3d}     {line[1].astype(int):>3d}       {line[2].astype(int):>3d}      Undefined      \n'

        s += '\n'
        if self.mass is not None:
            s += f'Mass: {self.mass:.3f} kg \n'
        else:
            s += 'Mass: Undefined \n'

        if self.cost is not None:
            s += f'Cost: $ {self.cost:.2f} \n '
        else:
            s += 'Cost: Undefined \n'
        return s

    def plot(self, domain=None, loads=None, fixtures=None,
             deflection=False, load_scale=None, def_scale=100, ax=None, fig=None):
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
        nodes = np.concatenate(
            (self.user_spec_nodes.copy(), self.rand_nodes.copy()))
        # mark self connected nodes
        self.edges[self.edges[:, 0] == self.edges[:, 1]] = -1
        con = self.edges.copy()
        matl = self.properties.copy()

        # remove self connected edges
        matl = matl[(con[:, 0]) >= 0]
        con = con[(con[:, 0]) >= 0]
        matl = matl[(con[:, 1]) >= 0]
        con = con[(con[:, 1]) >= 0]
        con = con.astype(int)

        num_nodes = nodes.shape[0]
        num_con = con.shape[0]

        size_scale = (nodes.max(axis=0)-nodes.min(axis=0)).max()
        if load_scale is None and loads is not None:
            load_scale = size_scale/np.abs(loads).max()/5

        if ax is None:
            fig = plt.figure()
            ax = fig.gca(projection='3d')

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

        edge_vec_start = nodes[con[:, 0], :]
        edge_vec_end = nodes[con[:, 1], :]

        # ****
        for i in range(num_con):
            # fig.canvas.flush_events()
            ax.plot([edge_vec_start[i, 0], edge_vec_end[i, 0]],
                    [edge_vec_start[i, 1], edge_vec_end[i, 1]],
                    [edge_vec_start[i, 2], edge_vec_end[i, 2]], 'k-')
            # fig.canvas.draw()

            # ax.draw() #sfr
        # ****

        if loads is not None:
            ax.quiver(nodes[:, 0], nodes[:, 1], nodes[:, 2],
                      loads[:, 0, 0], loads[:, 1, 0], loads[:, 2, 0],
                      length=load_scale, pivot='tip', color='r')

        if fixtures is not None:
            fix_nodes = nodes[fixtures[:, :, 0].any(axis=1)]
            ax.scatter(fix_nodes[:, 0], fix_nodes[:, 1], fix_nodes[:, 2],
                       c='g', marker='o', depthshade=False, s=100)

        # plt.show()
