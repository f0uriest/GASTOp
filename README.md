# APC524_FinalProject
Genetic Algorithm for Topological Optimization of Structures

Overview: Implement genetic algorithm for topological optimization of structures


Data Type: chromosome
    Contains: list of nodes, list of connections, list of materials, (list of x-sections?)

Function: main
    Inputs:
        Envelope dimensions
        Number of nodes
        Number of members
        Fixed nodes
        Load scenarios
        Interference regions
        Fixed nodes
        Material properties
        Population size
        Number of generations
        Convergence criteria/tolerances
    Outputs:
        “Optimal” design
        Fitness score/weight/other parameters

Function: Make a new chromosome
    Inputs:
        Number of nodes
        Number of members
        Range of nodes
        Fixed nodes
    Output:
        chromosome

Function: crossover - combines two chromosomes
    Inputs
        Parent chromosome 1
        Parent chromosome 2
        Crossover criteria (ie, where to split, which half to take, etc)
    Output
        Child chromosome
    
Function: Mutation - perturbs some chromosome
    Inputs:
        Parent chromosome
        Mutation parameters (which genes get mutated, by how much. std dev for rng)
    Outputs:
        Mutated chromosome

Function: Selector - chooses which from current generation get passed on
    Inputs:
        Chromosomes from current generation
        Fitness values for each chromosome
        Ratios of mutation to crossover to new chromosomes
    Outputs:
        Chromosomes for next generation

Function: fitness function
    Inputs:
        FoS
        Weight
        Interferences
        Misc other parameters
    Outputs:
        Fitness score

Function: Structural analysis 
    Inputs
        Chromosome
        Applied Loads
    Ouputs
        Factor of safety

Function: mass
    Inputs
        Chromosome
    Outputs
        Mass of structure

Function: Interferences
    Inputs
        Chromosome
        Areas where interferences matter (ie, places where there shouldn’t be beams)
    Outputs:
        Number of interferences
        ID of interfering members?

Function: plotter
    Inputs
        Chromosome
    Outputs
        Graphic of structure

Function: progress monitor
    Inputs
        Chromosomes
        Fitness scores
    Outputs
        Graphs of fitness vs time


