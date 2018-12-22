import numpy as np
import utilities
import Truss


class Eval():
    # wrapper for structural analysis,
    #
    def __init__(self, struct_solver, mass_solver, interferences_solver, boundary_conditions, properties_dict):
        self.struct_solver = getattr(self, struct_solver)
        self.mass_solver = getattr(self, mass_solver)
        self.interferences_solver = getattr(self, interferences_solver)
        self.boundary_conditions = boundary_conditions
        self.properties_dict = properties_dict

        # df.at[0,'A']
        # t2 = df.iloc[[4,4,3,4],[1]]
        '''
                  A         B         C
            0 -0.074172 -0.090626  0.038272
            1 -0.128545  0.762088 -0.714816
            2  0.201498 -0.734963  0.558397
            3  1.563307 -1.186415  0.848246
        '''

    def mat_struct_analysis_DSM(self, truss):
        """Calculates deflections and stresses using direct stiffness method.

        Constructs global stiffness matrix from nodes and connections, 
        and computes deflections under each loading scenario.
        From deflections, calculates internal forces, stresses, and factor 
        of safety in each member under each loading scenario

        Args:
            truss (Truss object): Truss to be evaluated. Must have nodes,
                edges, and properties defined.

        Returns:
            FoS (ndarray): 2D array of factor of safety values. First index 
                corresponds to members, second index corresponds to different
                loading scenarios. Factor of safety is defined as the materials
                yield strength divided by the von Mises stress in the member.
                If structure is statically indeterminate under a given loading
                scenario, FoS will be zero.
                FoS in member i under loading j is FoS[i, j]
            V (ndarray): 3D array of node deflections. Distances in meters,
                angles in radians. First index corresponds to node number,
                second index is deflections in x,y,z coordinates, and rotations
                about x,y,z axes. The third axis corresponds to different
                loading scenarios.
                Deflection at node i under loading j is V[i, :, j] = 
                [dx, dy, dz, d_theta_x, d_theta_y, d_theta_z]
        """

        # make local copies of arrays in case something breaks
        nodes = np.concatenate(
            (truss.user_spec_nodes.copy(), truss.rand_nodes.copy()))
        # mark self connected nodes
        truss.edges[truss.edges[:, 0] == truss.edges[:, 1]] = -1
        con = truss.edges.copy()
        matl = truss.properties.copy()
        loads = self.boundary_conditions['loads']
        fixtures = self.boundary_conditions['fixtures']

        # remove self connected edges
        matl = matl[(con[:, 0]) >= 0]
        con = con[(con[:, 0]) >= 0]
        matl = matl[(con[:, 1]) >= 0]
        con = con[(con[:, 1]) >= 0]

        num_nodes = nodes.shape[0]
        num_con = con.shape[0]
        num_loads = loads.shape[2]

        # get material properties etc
        E = self.properties_dict['elastic_modulus'][matl]
        G = self.properties_dict['shear_modulus'][matl]
        YS = self.properties_dict['yield_strength'][matl]
        A = self.properties_dict['x_section_area'][matl]
        Iz = self.properties_dict['moment_inertia_z'][matl]
        Iy = self.properties_dict['moment_inertia_y'][matl]
        J = self.properties_dict['polar_moment_inertia'][matl]
        OD = self.properties_dict['outer_diameter'][matl]

        # initialize empty matrices
        # member stiffness matrices in local coords
        Kloc = np.zeros((12, 12, num_con))
        # member stiffness matrices in global coords
        KlocT = np.zeros((12, 12, num_con))
        Kglob = np.zeros((6*num_nodes, 6*num_nodes))  # global stiffness matrix
        Q = np.zeros((num_con, 12))  # end forces on members
        Ei = np.zeros((num_con, 12))  # local to global matrix indices
        V = np.zeros((num_nodes, 6, num_loads))  # displacements
        r = np.zeros((3, 3, num_con))  # member rotation matrices
        # local to global transformation matrix
        T = np.zeros((12, 12, num_con))
        k1 = np.zeros((3, 3, num_con))  # stiffness matrix components
        k2 = np.zeros((3, 3, num_con))  # stiffness matrix components
        k3 = np.zeros((3, 3, num_con))  # stiffness matrix components
        k4 = np.zeros((3, 3, num_con))  # stiffness matrix components
        FoS = np.zeros((num_con, num_loads))  # factor of safety

        # calculate vectors of members in global coords
        edge_vec = nodes[con[:, 1], :] - nodes[con[:, 0], :]
        L, b, a = utilities.cart2sph(
            edge_vec[:, 0], edge_vec[:, 1], edge_vec[:, 2])
        ca = np.cos(a)  # a is azimuthal angle
        sa = np.sin(a)
        cb = np.cos(b)  # b is elevation angle
        sb = np.sin(b)

        # populate transformation matrices
        r[0, 0, :] = cb*ca
        r[0, 1, :] = sb
        r[0, 2, :] = sa*cb
        r[1, 0, :] = -sb*ca
        r[1, 1, :] = cb
        r[1, 2, :] = -sb*sa
        r[2, 0, :] = -sa
        r[2, 2, :] = ca
        T[0:3, 0:3, :] = r
        T[3:6, 3:6, :] = r
        T[6:9, 6:9, :] = r
        T[9:12, 9:12, :] = r

        # stiffness matrix elements in x,y,z,theta
        co = np.stack((12*np.ones(num_con), 6*L, 4*L**2, 2*L**2), axis=1)
        x = (E*A)/L  # axial stiffness along x
        y = (((E*Iy)/(L**3))*co.T).T  # bending stiffness about y
        z = (((E*Iz)/(L**3))*co.T).T  # bending stiffness about z
        g = G*J/L  # torsional stiffness about x axis

        # form stacked local stiffness matrices
        k1[0, 0, :] = x
        k1[1, 1, :] = z[:, 0]
        k1[2, 2, :] = y[:, 0]
        k2[1, 2, :] = z[:, 1]
        k2[2, 1, :] = -y[:, 1]
        k3[0, 0, :] = g
        k3[1, 1, :] = y[:, 2]
        k3[2, 2, :] = z[:, 2]
        k4[0, 0, :] = -g
        k4[1, 1, :] = y[:, 3]
        k4[2, 2, :] = z[:, 3]
        k2t = np.transpose(k2, axes=(1, 0, 2))
        kr1 = np.concatenate((k1, k2, -k1, k2), axis=1)
        kr2 = np.concatenate((k2t, k3, -k2t, k4), axis=1)
        kr3 = np.concatenate((-k1, -k2, k1, -k2), axis=1)
        kr4 = np.concatenate((k2t, k4, -k2t, k3), axis=1)
        Kloc = np.concatenate((kr1, kr2, kr3, kr4), axis=0)

        # construct global stiffness matrix from element matrices
        for ii in range(num_con):
            # get member indices to global stiffness matrix
            e = np.concatenate((np.arange(6*con[ii, 0], 6*con[ii, 0]+6),
                                np.arange(6*con[ii, 1], 6*con[ii, 1]+6)), axis=0)
            # transform from local to global coords
            KlocT[:, :, ii] = np.matmul(Kloc[:, :, ii], T[:, :, ii])
            # form global stiffness matrix
            Kglob[np.ix_(e, e)] = (Kglob[np.ix_(e, e)] +
                                   np.matmul(T[:, :, ii].T, KlocT[:, :, ii]))
            Ei[ii, :] = e  # save indices for later

        # calculate displacements
        for j in range(num_loads):
            # set unconnected nodes to fixed
            unconnected = np.setdiff1d(range(num_nodes), con.flatten())
            fixtures[unconnected] = 1
            # make sure loaded nodes are not fixed
            fixtures[:, :, j][loads[:, :, j].any(axis=1)] = 0
            # get indices of free nodes
            f = np.nonzero(
                1-np.ravel(fixtures[:, :, j]))
            f = f[0]  # get array out of tuple

            # solve for displacements of free nodes
            try:
                np.ravel(V[:, :, j])[f] = np.linalg.solve(
                    Kglob[np.ix_(f, f)], np.ravel(loads[:, :, j])[f])
            # if matrix is singular, stop, FoS still all zeros
            except np.linalg.LinAlgError:
                return FoS, V

            # calculate forces and stresses
            for i in range(num_con):
                # end forces
                Q[i, :] = np.matmul(
                    KlocT[:, :, i], np.ravel(V[:, :, j])[Ei[i, :].astype(int)])
                # combined moment about y, z
                M = np.sqrt(Q[i, 4]**2 + Q[i, 5]**2)
                # axial stress due to bending moment
                sigmaXbending = M*OD[i]/(2*Iz[i])
                # axial stress due to axial forces
                sigmaXaxial = np.abs(Q[i, 0]/A[i])
                # transverse stress due to torsion
                tauTorsion = Q[i, 3]*OD[i]/(2*J[i])
                # transverse stress due to shear
                tauXY = 2*np.sqrt(Q[i, 1]**2 + Q[i, 2]**2)/A[i]
                # determine von mises stress
                sigmaVM = np.amax((np.sqrt((sigmaXbending+sigmaXaxial)**2 +
                                           3*tauTorsion**2), np.sqrt(sigmaXaxial**2 + 3*tauXY**2)))
                # factor of safety in each beam under each loading condition
                if sigmaVM > 1e-6:
                    FoS[i, j] = YS[i]/sigmaVM
                else:
                    FoS[i, j] = 1e6

        return FoS, V

    def mass_basic(self, truss):
        """Calculates mass of structure

        Considers only members, does not account for additional mass due
        to welds or connection hardware.

        Args:
            truss (Truss object): Truss to be evaluated. Must have nodes,
                edges, and properties defined.

        Returns:
            mass (float): Mass of the structure in kg.
        """

        # make local copy of arrays in case something breaks
        nodes = np.concatenate(
            (truss.user_spec_nodes.copy(), truss.rand_nodes.copy()))
        # mark self connected nodes
        truss.edges[truss.edges[:, 0] == truss.edges[:, 1]] = -1
        con = truss.edges.copy()
        matl = truss.properties.copy()

        # remove self connected edges
        matl = matl[(con[:, 0]) >= 0]
        con = con[(con[:, 0]) >= 0]
        matl = matl[(con[:, 1]) >= 0]
        con = con[(con[:, 1]) >= 0]

        # calculate member lengths
        edge_vec = nodes[con[:, 1], :] - nodes[con[:, 0], :]
        L = np.sqrt(
            edge_vec[:, 0]**2 +
            edge_vec[:, 1]**2 +
            edge_vec[:, 2]**2)

        # get material properties
        A = self.properties_dict['x_section_area'][matl]
        dens = self.properties_dict['density'][matl]
        mass = np.sum(A*L*dens)

        return mass

    def interferences_ray_tracing(self, truss):
        pass

    def blank_test(self, truss):
        """Blank function used for testing GA when no evaluation needed"""
        return None, None

    def __call__(self, truss):

        fos, deflection = self.struct_solver(truss)
        mass = self.mass_solver(truss)
        interferences = self.interferences_solver(truss)
        truss.fos = fos
        truss.deflection = deflection
        truss.mass = mass
