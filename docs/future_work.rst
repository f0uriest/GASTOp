===========
Future Work
===========

One of the main work that remains is fixing how classes are set up in the program.
Currently, the methods that update the population (Mutator, Crossover, and
Selector) are base classes that contain multiple methods within each. Users
can specify which method within these classes they want to use for a specific
action such as for updating edges, nodes, or properties, for a specific run
of the program. However, when a Mutator object gets instantiated, it contains
all of the Mutator methods even though only one of those methods is going to be
used during the course of that run. This is inefficient.

A better way to handle this situation is by implementing Abstract Base Classes
(ABCs), which will be done to improve the quality of the program. The goal is
to redefine Mutator, Crossover, and Selector classes as ABCs which contain
some *run* method. Note that the *run* method will not be defined in the ABC
itself. The current methods for Mutator, Crossover, and Selector will then
be defined as subclasses of its corresponding ABC. For example, the gaussian
Mutator method will now become a subclass of the ABC Mutator. Gaussian
subclass will contain a *run* method which performs the gaussian mutation. Now
a Gaussian Mutator object can get instantiated instead of a Mutator object as
a whole which contains unnecessary information from the program's point of
view.

This change must be made along with a modification to the routine that
instantiates a Mutator, Crossover, or Selector object. Currently, one of
these objects is first instantiated and the ``__call__`` method within the object
contains an argument that specifies the method that should be run. There are
several ways to modify this routine to make it work with the ABC implementation.
One method is to create a function that takes as input the user's choice for
mutation, crossover, and selection. The function then instantiates the correct
objects and returns 3 objects: a specific type of Mutator, a specific type
of Crossover, and a specific type of Selector. When a mutation needs to be done,
the *run* method of the instantiated Mutator object can now be directly called.
