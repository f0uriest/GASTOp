import numpy as np

# Specify set-up things
#declare all variables (will call the function to parse the input file later)

# Create the Genetic Algorithm Object
ga = GenAlg(blah)

# Create the Evaluator Object
evaluator = Eval(blah)

# Create a Fitness Function Object
fit = FitnessFunction(blah)
# Create all of the first elements
population = [ga.generate_random for i in range(ga.pop_size)] # List of trusses

for j in range(ga.num_generations): # Loop over all generations:
    for i in range(ga.pop_size): # Loop over all beams -> PARALLELIZE. Later
        evaluator(population[i]) # Run evaluator method. Will store results in Truss Object
        fit(population[i]) # Assigns numerical score to each truss
    population = ga.update_population(population) # Determine which members to
    ga.progress_monitor(population)

### Read in the Possible Materials input file and create objects for each one
"""
Call function to build beam dictionary. Put function in utilities.
"""
material_dict = create_material_dict(input_file)
