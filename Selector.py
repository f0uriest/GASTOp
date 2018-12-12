import math
import random

class Selector(): # Cristian
    '''
    Selects parents to be used for crossover and mutation.

    Selector() object takes number of parents to create and current population,
    and returns parents as list of indices in corresponding population.
    '''
    def __init__(self,sel_params):
        self.sel_params = sel_params

    def inverse_square_rank_probability(self,num_parents,population):
        '''
        First, sorts population by fitness_score.
        Creates a list, with each entry 1/sqrt(N) for N = 1, ...
        Random values are then produced between the largest and smallest
        elements of the list. The index of this reference list that the
        random value falls between is the index of the chosen parent.
        In this way, the most probable parents are those with the highest
        fitness scores.
        '''

        population.sort(key=lambda x: x.fitness_score, reverse=True)
        # print([x.fitness_score for x in population])

        pop_size = len(population)
        reference_list = [1/math.sqrt(n) for n in range(1,pop_size+1)]
        # print(reference_list)

        # Initialize a list of zeros for the parent indices. For each requested
        # parent, randomly generate a number between the bounds of the reference
        # list. Find the index in the reference list where the random value
        # falls. For example, if the random value were 0.6, the corresponding
        # index would be 1 since 0.6 lies between 1/sqrt(2) and 1/sqrt(3).
        parents = [0]*num_parents
        for i in range(num_parents):
            rand_val = random.uniform(1/math.sqrt(pop_size+2),1)
            for j,val in enumerate(reference_list):
                if rand_val < val:
                    parents[i] = j
                else:
                    break

        return parents

    def __call__(self,num_parents,population):
        method = getattr(self,self.sel_params['method'])
        parents = method(num_parents,population)
        return parents
