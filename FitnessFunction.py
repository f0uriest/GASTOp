class FitnessFunction(): # Rory
    # equation: string flag to denote which hard-coded method to use
    # weights: numpy array

    def __init__(self,equation,parameters):
        self.equation = equation # function handle
        self.parameters = parameters # list

    def sum_of_squares(self,truss):
        # Hard coded equation that takes in
        pass

    def __call__(self,truss):
        equation = getattr(self,self.equation)
        equation(truss)
