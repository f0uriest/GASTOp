===============
Lessons Learned
===============

Through this project, we learned numerous invaluable lessons which have ultimately
made us better programmers. We spent a lot of time up front to think through the
project as a group before starting to write any code. During these meetings,
we designed the interface of our program, organized the class hierarchy, outlined
the code structure, and divided up the work between the group members. These
initial design meetings helped us to be organized and avoided merge conflicts.

Several tools were also used during the course of this project. We learned and
implemented automated testing (Travis CI) which made it easier to debug the code.
Coveralls were used to track how much of the program was covered by tests, and
Codacy was used to identify issues with the code and to track/improve code
quality. These are practical tools that we are now exposed to and can utilize
in other projects outside of this course.

Coding specific lessons to improve the performance of the program were also
learned. By making mistakes, we learned that vectorization and logical
indexing are almost always a more efficient alternative as opposed to
*for* loops and *if* statements. Furthermore, although we've learned about
profiling tools and techniques, this project gave us an opportunity to apply
that knowledge to something substantial. When profiling, it is important to
begin with the highest level of software architecture. After identifying
hotspots (i.e. functions where the code spent most of the time), it is
important to check which lines in the function call require the most time.
In this way, the bottleneck can be easily found and fixed.

We also learned a little about programming in parallel. Initially, we wrote the
whole project to run in serial, and while it ran in a reasonable amount of time
for our purposes, it was not very scalable. As a result, we looked into
re-writing elements of the architecture to be performed in parallel. Because we
wrote the application in python, there are already many libraries written to
parallelize *for* loops and other code structures that can be easily parallelized,
but as a result many of the design decisions about what's going on behind the
scenes at the system levels are not made by the user. In the end, we decided to
implement a multithreading design for the program using python's
pool module from the multithreading library. In addition to learning about how
to break apart different operations in a multithreading environment, there were
also some unexpected issues that arose regarding random number generation seed.
In order to produce repeatable results during the design process, the random
number generator seed was specified. But when threads that created random
numbers were created, the random number generator seed was not carried through
to the individual threads. We also ran into some issues in how python passes
around object pointers instead of the object itself with the multithreading
design because it expects every function to pass something back instead of
simply providing an object which is edited in its place. Issues such as these
were identified by implementing well-designed unit tests from the beginning of
the design creation.


Design Decisions
================

GenAlg
******
The primary design decision for GenAlg was to have it be the driver for all of
the other classes and their respective functions. Originally, we had designed
the program to run with a main.py driver and have Genalg simply be the interface
between this driver script and the rest of the classes. But then we realized
that it would be more efficient to have Genalg orchestrate everything.
Especially once we moved to a multithreading design, it made more sense to have
function calls performed closer to the objects they are editing so that there
was a smaller chance multiple threads would ever have the possibility of trying
to read/write to the same object at once.

Evaluator
*********
The majority of the design and coding time in the Evaluator class went into the matrix
structural analysis method. We initially planned on using an existing open source code and
then improving upon it, but after comparing several options, we found that none of the codes
available were particularly well designed, and most lacked sufficient documentation,
and would require a nearly ground up rewrite. We therefore decided to implement our own from
the beginning. We consulted several books on matrix structural analysis to understand the
basic operations the function must perform, and examined existing codes for basic structure
and things to improve upon.

One issue we found with many existing codes was that they computed the element stiffness matrices
individually, one by one. This is both inefficient and made the code difficult to read. We instead
constructed these matrices in a vectorized manner, where all the matrices were created at once in a stacked
3D array. Another issue with most of the open source codes we looked at was they simply did too many and
offered too many options. For example, they allowed for pinned or hinged connections between members,
distributed loads applied to members in various shapes and configurations, non-axisymmetric beams, and other
functionality that while desirable in a full featured structural solver, simply added unneeded complexity in
our case. Given the number of iterations our method would be expected to run for, we attempted to only include
functionality that would be absolutely necessary and that would work with the random nature of the structures generated.
For example, applying a distributed load to a member is impossible if the member only exists in certain trusses but not in others.
Similarly, allowing for hinged connections or twisted members is meaningless to implement if joints and members are distributed randomly.

Truss
*****
The truss class was initially designed as a simple data structure, with no methods. Over time, we realized that it made sense to include
plot and print methods in the truss class, rather than as utility functions. We also found that several methods in the Evaluator class
required not the "raw" truss data, but a "cleaned" version, where self connected and duplicate members were removed. Initially this functionality
was implemented separately in each function, but we realized this would be much more efficient as methods of the truss class, so that
each truss has the ability to mark its own invalid edges, and return data in a form used by the other methods in the program.

FitnessFunction
***************
An early decision made was to separate the evaluation and scoring of the trusses. This was primarily done to ease development,
so that we could build the core genetic algorithm components and test them with simple fitness functions before implementing the structural
analysis component. This also makes the program more general purpose, so that it can be used to optimize any function, unrelated to structural
problems. Of the four methods in the FitnessFunction class, three were implemented only for testing, to ensure that the genetic algorithm
could solve general optimization problems before specializing it for structural design. The structural fitness function allows the user
to optimize for several different factors in different degrees of importance by merely changing the weight factors.

Mutator
*******
The mutator class contains multiple methods so that the user can apply different
mutator methods to mutate different components of the truss - for example, the
user may choose to apply a *gaussian* mutation for the nodes but a *pseudo_bit_flip*
mutation for the edges. We wrote a __call__ method for the mutator class, allowing
us to *call* the mutator object on a truss. All of the methods in the mutator class
take in one parent numpy array and return one child numpy array. An issue with the
mutator class, more specifically with the gaussian method, was the some elements
were being mutated out of the user specified domain. In order to fix this issue,
we incorporated a periodic boundary condition which means the values that went
out of the boundary are going to be wrapped around into the domain on the other side
by the same amount that it went out of the boundary. In order to improve run-times,
we found any particular method which was taking up more time than other function calls
and made the code more efficient by using logical indexing and vector expressions
instead of the initial 'for' loop implementations.

Selector
********
Much like the Mutator, Crossover, and FitnessFunction classes, the Selector class was structured to contain multiple methods of selecting parents for crossover and mutation. The idea was to modularize the selection process, allowing new selection methods to easily be added as additional methods of the class. Selector objects return numpy arrays of indices of trusses in the current population. Alternatively, we could have decided to have the selector objects return the actual parent trusses, but this would require more memory than a simple index. Instead, the trusses are extracted from the population with the index when needed, upon performing crossover and mutation. Both currently implemented methods of performing selection make use of numpy arrays and built-in vectorized numpy functions. Initial for-loop implementations of the methods were significantly slower.


Crossover
*********
The crossover class contains multiple methods that can be used to perform crossover.
All of the crossover methods takes in two parent numpy arrays and returns two child
arrays. The decision to return two child arrays instead of one was made to ensure
that all possible "solutions" are explored. The reason it's possible to create two
child arrays is due to the dual nature of the crossover methods. For example, a one
point split can be done by splitting the parent arrays at a certain point and by
combining the first half of parent A with the second half of parent B or vice versa.
Thus, two children are possible.
