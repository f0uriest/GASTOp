class Eval():
    # wrapper for structural analysis,
    #
    def __init__(self,struct_solver,mass_solver,interferences_solver,boundary_conditions,beam_dict):
        self.struct_solver = struct_solver # function handle
        self.mass_solver = mass_solver # function handle
        self.interferences_solver = interferences_solver # function handle
        self.boundary_conditions = boundary_conditions # BC object
        self.beam_dict = beam_dict # pandas dataframe

        #df.at[0,'A']
        #t2 = df.iloc[[4,4,3,4],[1]]
        '''
                  A         B         C
            0 -0.074172 -0.090626  0.038272
            1 -0.128545  0.762088 -0.714816
            2  0.201498 -0.734963  0.558397
            3  1.563307 -1.186415  0.848246
        '''
    def mat_struct_analysis_DSM(self,truss):
        pass

    def mass_basic(self,truss):
        pass

    def interferences_ray_tracing(self,truss):
        pass

    def __call__(self,truss):
        struct_solver = getattr(self,self.struct_solver)
        mass_solver = getattr(self,self.mass_solver)
        struct_solver(truss)
        mass_solver(truss)
