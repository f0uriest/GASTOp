import numpy as np
from gastop import utilities


class Evaluator():
    """Implements various methods for scoring the truss in different areas.

    Methods include calculations of mass, factor of safety, deflections, and
    interference with user specified areas.

    The class is designed to be instantiated as an Evaluator object which will
    fully evaluate a Truss object using specified methods and parameters.
    """

    def __init__(self, struct_solver, mass_solver, interferences_solver, boundary_conditions, properties_dict):
        """Creates an Evaluator callable object.

        Once created, the Evaluator can be called on a Truss object to 
        calculate and assign mass, factor of safety, deflections, etc
        to the truss.

        Args:
            struct_solver (str): Name of the method to be used for structural
                analysis and calculating fos and deflections, as a string.
                e.g. ``'mat_struct_analysis_DSM'``.
            mass_solver (str): Name of the method to be used to calculate mass.
                e.g. ``'mass_basic'``.
            interferences_solver (str): Name of method to be used to determine
                interferences. e.g. ``'interferences_ray_tracing'``.
            boundary_conditions (dict): Dictionary containing:

                - ``'loads'`` *(ndarray)*: Array of loads applied to the structure.
                  First index corresponds to the node where the load is applied,
                  second index is the force in x,y,z and moment about x,y,z,
                  third index is for multiple loading scenarios.
                - ``'fixtures'`` *(ndarray)*: Array of flags denoting whether a node
                  is fixed or free. First index corresponds to the node, the
                  second index corresponds to fixing displacements in x,y,z
                  and rotations about x,y,z. The third index corresponds to
                  multiple loading scenarios with different fixtures for each.
                  Values of the array are 0 (free) or 1 (fixed).

            properties_dict (dict): Dictionary containing beam properties.
            Entries should be 1D arrays, with length equal to the number of
            beam options. Each entry in the array is the value of the key
            property for the specified beam type. Properties include:

                - ``'OD'``: Outer diameter of the beam, in meters.
                - ``'ID'``: Inner diameter of the beam, in meters.
                - ``'elastic_modulus'``: Elastic or Young's modulus of the
                  material, in Pascals.
                - ``'yield_strength'``: Yield or failure strength of the 
                  material, in Pascals.
                - ``'shear_modulus'``: Shear modulus of the material, 
                  in Pascals.
                - ``'poisson_ratio'``: Poisson ratio of the material,
                  dimensionless.
                - ``'x_section_area'``: Cross sectional area of the beam,
                  in square meters.
                - ``'moment_inertia_y'``: Area moment of inertia about beams
                  y axis, in meters^4.
                - ``'moment_inertia_z'``: Area moment of inertia about beams
                  z axis, in meters^4.  
                - ``'polar_moment_inertia'``: Area moment of inertia about beams
                  polar axis, in meters^4. 
                - ``'dens'``: Density of the material, in kilograms per cubic meter.

        Returns:
            callable Evaluator object.


        """
        self.struct_solver = getattr(self, struct_solver)
        self.mass_solver = getattr(self, mass_solver)
        self.interferences_solver = getattr(self, interferences_solver)
        self.boundary_conditions = boundary_conditions
        self.properties_dict = properties_dict

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
            2-element tuple containing:

            - **fos** *(ndarray)*: 2D array of factor of safety values. First index 
              corresponds to members, second index corresponds to different
              loading scenarios. Factor of safety is defined as the materials
              yield strength divided by the von Mises stress in the member.
              If structure is statically indeterminate under a given loading
              scenario, fos will be zero.

              Factor of safety in member i under loading j is fos[i, j]

            - **deflections** *(ndarray)*: 3D array of node deflections.
              Distances in meters, angles in radians. First index corresponds
              to node number, second index is deflections in global  x,y,z
              coordinates, and rotations about global x,y,z axes. The third
              axis corresponds to different loading scenarios.

              Deflection at node i under loading j is deflections[i, :, j] = 
              [dx, dy, dz, d_theta_x, d_theta_y, d_theta_z]
        """
        # mark self connected nodes
        orig_num_edges = truss.edges.shape[0]
        truss.edges[truss.edges[:, 0] == truss.edges[:, 1]] = -1

        # mark duplicate edges
        truss.edges.sort()
        truss.edges = np.unique(truss.edges, axis=0)
        truss.edges = np.concatenate(
            (truss.edges, -1*np.ones((orig_num_edges-truss.edges.shape[0], 2))), axis=0)

        # make local copies of arrays in case something breaks
        nodes = np.concatenate(
            (truss.user_spec_nodes.copy(), truss.rand_nodes.copy()))
        con = truss.edges.copy()
        matl = truss.properties.copy()
        loads = self.boundary_conditions['loads'].copy()
        fixtures = self.boundary_conditions['fixtures'].copy()

        # remove self connected edges and duplicate members
        matl = matl[(con[:, 0]) >= 0]
        con = con[(con[:, 0]) >= 0]
        matl = matl[(con[:, 1]) >= 0]
        con = con[(con[:, 1]) >= 0]
        con = con.astype(int)

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

            # fix free node displacements
            # currently acts weird and gives wrong results if a node is fixed in one direction and free in another
            # calculate displacements
        for j in range(num_loads):
            # set unconnected nodes to fixed
            unconnected = np.setdiff1d(range(num_nodes), con.flatten())
            fixtures[unconnected, :, j] = 1
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
            mass (float): Mass of the structure in kilograms.
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
        con = con.astype(int)

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
        """Not implemented yet.

        TODO: method to determine if truss members are crossing into 
        user specified areas. Used when a structure must be designed around
        something, such as a passenger compartment or other design components.
        """
        pass

    def blank_test(self, truss):
        """Blank function used for testing GA when no evaluation needed

        Args:
            truss (Truss object): Dummy Truss object, no attributes required.

        Returns:
            2-element tuple of (None, None)
        """

        return None, None

    def __call__(self, truss):
        """Computes mass, deflections, etc, and stores it in truss object.

        Used when an Evaluator object has been created with the
        methods to be used and any necessary parameters.

        Args:
            truss (Truss object): truss to be evaluated. 

        Returns:
           None

        """

        fos, deflection = self.struct_solver(truss)
        mass = self.mass_solver(truss)
        interferences = self.interferences_solver(truss)
        truss.fos = fos
        truss.deflection = deflection
        truss.mass = mass
        return truss
