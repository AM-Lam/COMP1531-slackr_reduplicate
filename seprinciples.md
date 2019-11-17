## Problems
As we moved into the third iteration of the project improving our code meant
refactoring large sections of the codebase. In order to do this we first had
to identify areas of the codebase that were under-par and then re-write the
problem areas by applying stricter standards of style to our code.

At the end of the second iteration our code had a large number of problems due
to poor design, the design smells that applied particularly strongly to our
code were:

#### Rigidity, Viscosity and Immobility: 
As all the functionality of our code had been put into separate files and each person in the team had written their own functions to do the same things, changes were difficult to implement and had to be re-written in multiple places making changes take a long time.

#### Fragility: 
A side-effect of the above was that changes to some areas of the codebase, mainly the datastructures, 
was liable to cause breakage across the entire project.

#### Needless Complexity: 
While not as large an issue as other smells, there were a number of areas in the code 
where things had been done in a needlessly complex way, part of this was due to a reticence to re-write datastructures after the initial stage of development.

#### Needless Repetition: 
The largest problem was this by far and most of the other problems in the code came as a result of this, since development across team-members wasn't communicated as effectively as it could have been. Each of us ended up re-writing code that other people had already completed.

#### Coupling: 
The final major issue was coupling, as each function was placed in its own file there was very little connection between related parts of code.


## Fixes

#### Reusability
So from  the problems identified above it became clear that when refactoring we should focus largely upon making our code more reusable and flexible so that it could be reused in multiple places. To do this we identified areas of the code that had similar or identical functionality then reproduced that functionality in the database.py file. This meant that whenever this functionality was needed we could call it from a single place. The impact of this was that the code was much easier to reuse in several places and changes, both large and small, were much faster and safer to implement. Some of the specific functions we used this for were:

- Verifying a token and returning a u_id
- Getting channel, user and message objects by id
- Checking a password/email combo was valid
- Changing attributes on an object (for example the text of a message)

#### Understandable
In order to deal with the complexity of our code we ensured that the entire codebase was commented appropriately and used appropriate variable and function names. We also stuck closely to the PEP-8 for style and aimed for a 10/10 pylint score. In order to achieve this, however, we needed to ignore some problems brought up by the linter but we believe these are defensible choices.

#### Maintainability
By condensing the functions that were once spread out over several files into ones related to what domain they touched (users, channels, etc.) and reducing the amount of repeated code we significantly increased maintainability by increasing the speed and ease with which code can be read and changed. Importantly these changes also made it easier to look at the interconnections between different parts of the code and thus prevents accidentally breaking one piece of code by changing another.

#### Testable
By ensuring that our code stuck closely to the spec in terms of input and output, this made it easy to have specific tests with predetermined input and output. Furthermore, in order to speed up testing and make it more generic we added decorators to our tests that allowed us to abstract away a lot of the boiler plate setting up code and focus on writing effective tests. All-in-all we have close to 100% coverage although there a few edge cases that were difficult to test, bringing it down to 98%.