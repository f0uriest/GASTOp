===============
Lessons Learned
===============

Through this project, we learned numerous invaluable lessons which have ultimately
made us better programmers. We spent a lot of time up front to think through the
project as a group before starting to to write any code. During these meetings,
we designed the interface of our program, organized the class heirarchy, outlined
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
indexing area almost always a more efficient alternative as opposed to
*for* loops and *if* statements. Furthermore, although we've learned about
profiling tools and techniques, this project gave us an opportunity to apply
that knowledge to something substantial. When profiling, it is important to
begin with the highest level of software architecture. After identifying
hotspots (i.e. functions where the code spents most of the time), it is
important to check which lines in the function call require the most time.
In this way, the bottleneck can be easily found and fixed.
