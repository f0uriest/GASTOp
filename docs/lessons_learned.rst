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
implement a multithreading design for the program (where functional) python's
pool module from the multithreading library. In addition to learning about how
to break apart different operations in a multithreading environment, there were
also some unexpected issues that arose regarding random number generation seed.
In order to produce repeatable results during the design process, the random
number generator seed number was specified. But when threads that created random
numbers were created, the random number generator seed was not carried through
to the individual threads. We also ran into some issues in how python passes
around object pointers instead of the object itself with the multithreading
design because it expects every function to pass something back instead of
simply providing an object which is edited in its place. Issues such as thse
were identified by implementing well-designed unit tests from the beginning of
the design creation.

# How do you make a new section?
--- New section: Design decisions ---
Genalg:
The primary design decision for Genalg was to have it be the driver for all of
the other classes and their respective functions. Originally, we had designed
the program to run with a main.py driver and have Genalg simply be the interface
between this driver script and the rest of the classes. But then we realized
that it would be more efficient to have Genalg orchestrate everything.
Especially once we moved to a multithreading design, it made more sense to have
function calls performed closer to the objects they are editing so that there
was a smaller chance multiple threads would ever have the possibility of trying
to read/write to the same object at once.
