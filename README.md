<!----- Conversion time: 2.094 seconds.


Using this Markdown file:

1. Cut and paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* GD2md-html version 1.0β13
* Tue Nov 13 2018 16:16:50 GMT-0800 (PST)
* Source doc: https://docs.google.com/open?id=1g0me5MhVhH0BrnZtYyu4_-fo4UKtilzCmW2_JjDGbHU
* This is a partial selection. Check to make sure intra-doc links work.
----->


Overview: Implement genetic algorithm for topological optimization of structures

**Data Type: chromosome [10%]**

	Contains: list of nodes, list of connections with ID for materials properties

	Method: sort self

**Input format and parsing [5%]**

**Function: main [10%]**

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

**Function: Make a new chromosome [5%]**

Inputs:

		Number of nodes

		Number of members

		Range of nodes

		Statistical variances for each area

		Fixed nodes

		Dictionary for matl properties

	Output:

		Chromosome object

**Function: crossover - combines two chromosomes [5%]**

	Inputs

		Parent chromosome 1

		Parent chromosome 2

		Crossover criteria (ie, where to split, which half to take, etc) [equal number of 1's and 0's for each parent, and then 'link' the 1's and the 0's]

	Output

		Child chromosome object

	

**Function: Mutation - perturbs some chromosome [5%]**

	Inputs:

		Parent chromosome

		Mutation parameters (which genes get mutated, by how much. std dev for rng)

		Parameter limits

	Outputs:

		Mutated chromosome

**Function: Selector - chooses which from current generation get passed on [10%]**

Calls the mutation, crossover, makenew gene functions

Options:

		Check for population diversity and change the next generation accordingly

Inputs:

		Chromosomes from current generation (list of chromosome objects)

		Fitness values for each chromosome

		Ratio of mutation to crossover to new chromosomes?

	Outputs:

		Chromosomes for next generation

**Function: fitness function [5%]**

Calls structural function, weight function

Should make parameters

Inputs:

	Current gen chromosome

	Acquires these from calling other functions:

		FoS

		Weight

		Interferences

		Misc other parameters

	Outputs:

		Fitness score

**Function: Structural analysis [5-35%]**

Calls the Mass Function

-if stiffness matrix is not invertible, exit

	Inputs

		Chromosome object

		Applied Loads

	Outputs

		Factor of safety

		Mass

**Function: mass [5%]**

	Inputs

		Length of Connections

		Material Reference File

	Outputs

		Mass of structure

**Function: Interferences [15%]**

(Ray tracing)	

Decide when its run and what it does when there are interferences

-drop and make new chromosome?

-delete offending members?

-weight base on how much is in box?

Inputs

		Chromosome

		Areas where interferences matter (ie, places where there shouldn't be beams)

	Outputs:

		Number of interferences

		ID of interfering members?

**Function: plotter [20%] Susan?**

Options:


    One shows the constraint box and the bounding box and the loads


    One shows the design evolution


    One shows final structure, loaded structure, etc

	Inputs

		Chromosome

	Outputs

		Graphic of structure

**Function: progress monitor [10%]**

	Inputs

		Chromosomes

		Fitness scores

	Outputs

		Graphs of fitness vs time

**Documentation**

**Presentation**

**Project Timeline:**

Nov 7 is the deadline to email Gabe with a group and a rough sketch of the idea (3-6 people)

Nov 12-17 meeting with AI to discuss scope (20 mins)

**Late Nov **- design document submission & in class design review

**Dec 7th** - basic prototype demo

**Dec 14 **- alpha "0.1" version

**Jan 14** - presentation on project (20mins)

**Jan 15 **ish - submission deadline

**11/12 Meeting**

Decided to solve 2D structural, can up to 3D if we have time

First generation options:



*   User input
*   Randomly 

How to reproduce:



*   Direct Passover: just keep good ones
*   Mutation: randomly alter some of them
*   Cross-over: make combinations of good ones

Sort the entries of the chromosomes so that we can compare them so find duplicates

Have grid to lock nodes to?

Have selector know about population diversity?

Who does testing?

Ways to make it easier if it's harder than expected:



*   No interior restricted area & convex domain (removes the interference code)
*   Only use one method to create next generation

**For next meeting:**

Read some more so we can figure out work breakdown

Make flowchart (Susan/Rory)

Find 2D structural analysis code (Cristian) 


<!-- GD2md-html version 1.0β13 -->


![Pretty nifty, eh?](https://g.gravizo.com/source/svg?https%3A%2F%2Fraw.githubusercontent.com%2Ff0uriest%2FAPC524_FinalProject%2Fmaster%2Fflowchart.gv)

