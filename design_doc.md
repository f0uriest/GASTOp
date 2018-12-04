# GASTOp:  Genetic Algorithm for Structural Design and Topological Optimization

**Group Members:** Rory Conlin (MAE), Paul Kaneelil (MAE), Cristian Lacey (MAE), Susan Redmond (MAE), Dan Shaw (MAE), Amlan Sinha (MAE)

## Introduction

Genetic algorithms are a class of methods for solving non-convex, nonlinear optimization problems based on ideas from evolutionary biology. They operate by generating a population of random "chromosomes" (test solutions to the problem), evaluating the fitness of each chromosome, and then creating a new "generation" by taking combinations of the fittest chromosomes from the last generation. This process is repeated for a fixed number of generations or until the fitness score stops decreasing.

In this case, we will create a genetic algorithm to design a structure (building, bridge, vehicle frame, chair, etc) while optimizing certain design criteria such as weight, number of connections, stiffness, and factor of safety. At it's most basic level, a structure can be thought of as a list of nodes (locations in x,y,z space), a list of connections between these nodes (ie, node 1 is connected to node 4, node 2 is connected to node 8 etc.), and specifications of material properties for each connection (ie, the beam between node 2 and node 3 is 1/2" diameter steel). 

The user will be able to input boundary conditions such as locations of fixed supports and applied loads, and the program will generate random structures and evaluate how well they match the desired criteria by using a matrix structural analysis code. The highest scoring designs will be mixed and combined by taking linear combinations of the vectors that define each structure and repeating until convergence.

## Program Outline

**Data Type: chromosome** - A wrapper for the three arrays that define the structure, with a method to sort itself so that two chromosomes can be meaningfully compared (ie, what you call node 1 someone else might call node 5, this is needed to resolve ambiguity).

	Contains: 
		array of nodes
		array of connections
		array for materials properties

	Method: sort self

**Function: Input format and parsing** - Read in user supplied data regarding boundary conditions, number of nodes, material properties etc. Initially this will be done with a text/csv file, with a stretch goal to incorporate a GUI or possibly accept output from CAD software as an initial design to improve upon.

**Function: main** - Driver program that calls other functions

	Inputs:

		Envelope dimensions

		Max & Min number of nodes

		Max & Min number of members

		Fixed nodes (Boundary Condition Locations)

		Load scenarios (Boundary Condition Loadings)

		Interference regions

		Material properties file (pointer)

		Population size for each generation

		Number of generations to be run

		Convergence criteria/tolerances (or just run a certain number and stop)

	Outputs:

		"Optimal" design

		Fitness score/weight/other parameters

		Plot of bounding box, boundary conditions, and loads

**Function: Make a new chromosome** - makes a random structure given certain parameters (envelope dimensions, number of nodes, etc).

	Inputs:

		Number of nodes

		Number of members

		Range of nodes

		Statistical variances for each area

		Fixed nodes

		Dictionary for material properties

	Output:

		Chromosome object

**Function: fitness function** - Determine fitness score for each structure by calling functions to perform structural analysis, interference checks, etc.

	Inputs:
	
		Current generation chromosome

	Outputs:

		Fitness score

**Function: Structural analysis** - Evaluate each structure under applied loads to determine deflections, factor of safety, etc.

	Inputs:

		Chromosome object

		Applied Loads/Boundary conditions

	Outputs:

		Factor of safety

		Mass

**Function: mass** - Determine mass of structure based on number and location of nodes and connections

	Inputs:

		Structure geometry

		Material Reference File

	Outputs:

		Mass of structure

**Function: Interferences** - (stretch goal) Checks that no structural members are passing through certain areas, using ray tracing techniques. ie, if you're designing a car, you need to make sure there's room for the engine and the passengers.

	Inputs:
	
		Chromosome

		Areas where interferences matter (ie, places where there shouldn't be beams)

	Outputs:

		Number of interferences

		ID of interfering members


**Function: Selector**  - Based on fitness scores for each chromosome, chooses which from current generation get passed on. Calls the mutation, crossover, makenew gene functions. Stretch goal: Check for population diversity and change the next generation accordingly, more options for doing selection (tournament, roulette, weighted random, etc).

	Inputs:

		Chromosomes from current generation (list of chromosome objects)

		Fitness values for each chromosome

		Ratio of mutation to crossover to new chromosomes?

	Outputs:

		Chromosomes for next generation


**Function: crossover** - Take two "parent" chromosomes and make a "child" chromosome by a linear combination of the parents. Stretch goal: offer more ways of doing crossover (ie, one point split, multipoint split, random comb etc).

	Inputs:

		Parent chromosome 1

		Parent chromosome 2

		Crossover criteria (ie, where to split, which half to take, etc)

	Output:

		Child chromosome object

	

**Function: Mutation** - Make a child by "mutating" a parent - randomly perturbing elements of the arrays. Stretch goal: more ways of doing mutation (ie, flipping indices)

	Inputs:

		Parent chromosome

		Mutation parameters (which genes get mutated, by how much. std dev for rng)

		Parameter limits

	Outputs:

		Mutated chromosome


**Function: plotter** - Displays a 3D rendering of a structure and its deformations under the applied loads.

	Inputs:
	
		Chromosome

	Outputs:

		Graphic of structure

**Function: progress monitor** - After each generation is evaluated, display statistics of population, and calculate population diversity (ie, are all the chromosomes the same? If they are, the next generation should have more randomness to prevent "inbreeding").

	Inputs:

		Chromosomes

		Fitness scores

	Outputs:

		Graphs of fitness vs time
		
		Population diversity score

![Flowchart](flowchart.png)

## Tools used

The program will be primarily written in Python 3, using numpy and scipy libraries for the numerical computations and matplotlib for visualization. Depending on performance, parts of the code may be farmed out to a faster langugage such as C++, Fortran, or Julia, though we will also explore performance optimization available within Python such as Numba and Cython. Parallelizing will be done within Python using the multiprocessing and mpi4py libraries.


## Project Timeline:

**Dec 7** - Barebones genetic algorithm working, no structural analysis. Fitness function is simply to minimize norm of a vector or something simple, to prove the optimization part works correctly.

**Dec 14** - Incorporate beta version of structural analysis, text/csv file input.

**Jan 1** - Plotter, progress monitor, optimization/performance tuning.

**Jan 7** - Stretch goals beta, Presentation on project

**Jan 15** - Final submission deadline




