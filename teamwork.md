**Reflect on your use of agile practices and how you worked as a team.**

_Your reflection should, at a minimum, include:_
  * _How often you met, and why you met that often_
  * _What methods you used to ensure that meetings were successful_
  * _What steps you took when things did not go to plan during iteration 3_
  * _Details on how you had multiple people working on the same code_

| Progress | Type of Work                         | Person in charge |
|----------|--------------------------------------|------------------|
| Week 8   | -ask for clarification               | Everyone         |
|          | -rebuild the database.py             | Everyone         |
|          | -modify the functions in iteration 2 | Everyone         |
|          | -Fix up the styles like the import * | Owen, Ann, Arpit |

|----------|--------------------------------------|------------------|
| Week 9   | -Finish the functions(x32)           | Everyone         |
|          | -Refactor the code from iteration 2  | Everyone         |
|          | -Add decorator                       | Owen, Ann, Arpit |

# From last iteration
- Things should be done last iteration
    Modifying the database and all the functions in the last iteration.
    Making the frontend connected with backend

# meeting detail
- 06/11 60 minutes Talked about what we can modify from last iteration and how can we improve the database.py.
- 13/11 60 minutes Talked about the outline of the database.py like what attributes to put into class user, channel and message


# What we have improved
In terms of communication, we have made a better use of communication tools. Whenever changes were made to testing files or other files like the
database or server, we made sure that everyone was updated with the changes and also put in comments making the changes easier to understand.
Since we merge more often, more of us proofread each others' code before we actually merge our code into master. We also refactored our code by adding 
decorators to our test cases and rewriting some of the functions based on the DRY and KISS principals. Lot of files were grouped into a single file based
on functionality like auth.py and their tests also grouped together to make the interface cleaner and easier to understand.
We worked as a group more often and reviewed and modifed code more often. Refactoring was done by everyone so we were not only in charge 
of part of the codes but also the project as a whole.

# Challenges that we faced as a team
## Merge conflict
In the third iteration we faced many merge conflicts because we decided to merge lots of different code files together based on each functions properties. 
To easily manage and handle these merge conflicts, we commited and pushed our code to master as often as possible when making changes that might have 
affected others. This allowed us to stay up to date with new changes and work togheter efficiently.

## Distance/Remote Communication
We could not get toghter and work or do stand-ups very often due to some of the team members living far from the university. We could not work very
effectively due to this and had to manage work and code over online chats and this slightly hindered our teams planning and execution.

# What we can improve next time
We need to improve communication between team members. It would be a good idea to have a pre-commit message script, that would not allow other team members
to commit their changes until all of the tests pass in order to make sure the code works, because sometimes non functional code was pushed.
Next time we should use more diagrams to design data structures like the database to decrease the number of changes that were constantly being made to the 
database.
