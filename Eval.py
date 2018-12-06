class Eval():
    # wrapper for structural analysis,
    #
    def __init__(self,struct_solver,mass_solver,interferences_solver,boundary_conditions,beam_dict):
        self.struct_solver = struct_solver
        self.mass_solver = mass_solver
        self.interferences_solver = interferences_solver
        self.boundary_conditions = boundary_conditions
        self.beam_dict = beam_dict
    def mat_struct_analysis_DSM(self,truss):
        pass

    def mass_basic(self,truss):
        pass

    def interferences_ray_tracing(self,truss):
        pass

    def __call__(self,truss):
        self.struct_solver(truss)
        self.mass_solver(truss)

        pass
