<<<<<<< HEAD
**Demonstrate software engineering design understanding**

_Refactor or add to your code from iteration 2 to utilise good software engineering design to make your code more maintainable. Use a range of principles discussed in lectures._

_As you modify your code, maintain a up to a 2 page markdown file that lists the key changes you've made in your code and why they've been made._

_Write this in `seprinciples.md`._
=======
As we moved into the third iteration of the project improving our code meant
refactoring large sections of the codebase. In order to do this we first had
to identify areas of the codebase that were under-par and then re-write the
problem areas by applying stricter standards of style to our code.

## Problems Areas

At the end of the second iteration our code had a large number of problems due
to poor design, the design smells that applied particularly strongly to our
code were:
- Rigidity, Viscosity and Immobility: as all the functionality of our code had 
  been put into separate files and each person in the team had written their
  own functions to do the same things changes were difficult to implement and
  had to be re-written in multiple places making changes take a long time to
  make.
- Fragility: A side-effect of the above was that changes to some areas of the
  codebase, mainly the datastructures, was liable to cause breakage across the
  entire project.
- Needless Complexity: While not as large an issue as other smells there were a
  number of areas in the code where things had been done in a needlessly complex
  way, part of this was due to a reticence to re-write datastructures after the
  initial stage of development.
- Needless Repetition: The largest problem was this by far and most of the other
  problems in the code came as a result of this, since development across team-
  members wasn't communicated as effectively as it could have been each of us
  ended up re-writing code that other people had already completed.
- Coupling: The final major issue was coupling, as each function was placed in
  its own file there was very little connection between related parts of code.
>>>>>>> 5519b5aa47727c7be6fcee5f1fa4be4abb599750
