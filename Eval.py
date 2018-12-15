import numpy as np
import utilities
import Truss


class Eval():
    # wrapper for structural analysis,
    #
    def __init__(self, struct_solver, mass_solver, interferences_solver, boundary_conditions, beam_dict):
        self.struct_solver = struct_solver
        self.mass_solver = mass_solver
        self.interferences_solver = interferences_solver
        self.boundary_conditions = boundary_conditions
        self.beam_dict = beam_dict

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
        '''Calculates deflections and stresses using direct stiffness method'''
        # NOT FINISHED
        nodes = np.concatenate(
            (boundary_conditions.user_spec_nodes, truss.nodes))
        # mark self connected nodes
        truss.edges[truss.edges[:, 1] == truss.edges[:2]] = -1
        con = truss.edges
        matl = truss.properties

        # remove self connected edges
        matl = matl[(con[:, 0]) >= 0]
        matl = matl[(con[:, 1]) >= 0]
        con = con[(con[:, 0]) >= 0]
        con = con[(con[:, 1]) >= 0]

        num_nodes = nodes.shape[0]
        num_con = con.shape[0]

        # get material properties etc
        E = beam_dict['elastic_modulus'][matl]
        G = beam_dict['shear_modulus'][matl]
        YS = beam_dict['yield_strength'][matl]
        A = beam_dict['x_section_area'][matl]
        Iz = beam_dict['moment_inertia_z'][matl]
        Iy = beam_dict['moment_inertia_y'][matl]
        J = beam_dict['polar_moment_inertia'][matl]
        OD = beam_dict['outer_diameter'][matl]

        # initialize empty matrices
        # member stiffness matrices in local coords
        Kloc = np.zeros((12, 12, num_con))
        # member stiffness matrices in global coords
        KlocT = np.zeros((12, 12, num_con))
        Kglob = np.zeros((6*n, 6*num_nodes))  # global stiffness matrix
        Q = np.zeros((num_con, 12))  # end forces on members
        Ei = np.zeros((num_con, 12))  # local to global matrix indices
        V = np.zeros((6, num_nodes))
        r = np.zeros((3, 3, num_con))  # member rotation matrices
        # local to global transformation matrix
        T = np.zeros((12, 12, num_con))
        k1 = np.zeros((3, 3, num_con))  # stiffness matrix components
        k2 = np.zeros((3, 3, num_con))  # stiffness matrix components
        k3 = np.zeros((3, 3, num_con))  # stiffness matrix components
        k4 = np.zeros((3, 3, num_con))  # stiffness matrix components

        # calculate vectors of members in global coords
        edge_vec = nodes[con[:, 1], :] - nodes[con[:, 0], :]
        L, b, a = utilities.cart2sph(
            edge_vec[:, 0], edge_vec[:, 1], edge_vec[:, 2])
        ca = np.cos(a)
        sa = np.sin(a)
        cb = np.cos(b)
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
        co = np.array([12*np.ones((num_con, 1)), 6*L, 4*L**2, 2*L**2])
        x = (E*A)/L
        y = ((E*Iy)/(L**3))*co
        z = ((E*Iz)/(L**3))*co
        g = G*J/L

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

        for i in range(num_con):
            # get member indices to global stiffness matrix
            e = np.concatenate((np.arange(
                6*Con[i, 0], 6*Con[i, 0]+6), np.arange(6*Con[i, 1], 6*Con[i, 1]+6)), axis=0)
            # transform from local to global coords
            KlocT[:, :, i] = np.matmul(Kloc[:, :, i], T[:, :, i])
            # form global stiffness matrix
            Kglob[e, e] = Kglob[e, e] + np.matmul(T[:, :, i].T, KlocT[:, :, i])
            Ei[i, :] = e

        # need to parse loads / fixtures
        # calculate deflections
        # calculate member forces
        # calculate stresses / FS

    def mass_basic(self, truss):
        '''Calculates mass of structure'''
        # NOT TESTED

        nodes = np.concatenate(
            (boundary_conditions.user_spec_nodes, truss.nodes))
        # mark self connected nodes
        truss.edges[truss.edges[:, 1] == truss.edges[:2]] = -1
        con = truss.edges
        matl = truss.properties

        # remove self connected edges
        matl = matl[(con[:, 0]) >= 0]
        matl = matl[(con[:, 1]) >= 0]
        con = con[(con[:, 0]) >= 0]
        con = con[(con[:, 1]) >= 0]

        # calculate member lengths
        edge_vec = nodes[con[:, 1], :] - nodes[con[:, 0], :]
        L = np.sqrt(
            edge_vec[:, 0]**2 +
            edge_vec[:, 1]**2 +
            truss.nodes[:, 2]**2)
        A = self.beam_dict['area'][matl]
        dens = self.beam_dict['density'][matl]
        mass = A*L*dens
        truss.mass = mass

    def interferences_ray_tracing(self, truss):
        pass

    def __call__(self, truss):
        struct_solver = getattr(self, self.struct_solver)
        mass_solver = getattr(self, self.mass_solver)
        struct_solver(truss)
        mass_solver(truss)
