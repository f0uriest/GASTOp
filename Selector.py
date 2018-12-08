class Selector(): #Cristitatini
'''
Selector() object takes number of parents to create and current population, and
returns parents as list of indices in population.
'''
    def __init__(self,sel_params):
        self.sel_params = sel_params

    def inverse_square_rank_probability(self,num_parents,population):
        '''Point is to select parents of crossover and mutation.

        sort population list by fitness_score
        probablity of truss index appearing in reference list is proportional to
        inverse square root of rank in sorted population.
        this list of truss indices is then randomly selected from to determine
        the parents for crossover and mutation.

        return indices list
        '''
        pass

    def __call__(self,num_parents,population):
        method = getattr(self,self.sel_params['method'])
        parents = method(num_parents,population)
        return parents
