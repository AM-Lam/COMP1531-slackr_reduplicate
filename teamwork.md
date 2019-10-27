| Progress | Type of Work                         | Person in charge |
|----------|--------------------------------------|------------------|
| Week 5   | -ask for clarification               | Arpit            |
|          | -build the server.py                 | Everyone         |
|          | -build the framework of the database | Owen, Ann        |
|----------|--------------------------------------|------------------|
| Week 6   | -Finish the functions(x32)           | Everyone         |
|          | -Finish the test cases               | Everyone         |
|          | -modifying the database              | Everyone         |

# From Iteration one
- Things should be done last iteration
Our task board is now divided into 3 catagories - user, channel and message. It helps to distinguish the characteristic of the functions.

# meeting detail
- 19/10 15 minutes (Owen and Ann) Talked about the flask operations and database.py
- 21/10 30 minutes Talked about the outline of the database.py like what attributes to put into class user, channel and message
- 23/10 1.5 hours (Group) Draft of server.py and database.py is done. Talked about what functions and possible test cases. And also adding some methods into the classes of database.py
- 15/10 15 minutes (Owen and Arpit) Debugging the stub functions. Discussing about integrating frontend and backend.

# Communication/Time management
Since iteration 1 was done a bit rush, we learn from it and we save time for integrating the whole project. We do realise we will need more time to merge the all the function together and produce a product and more test cases so we set the deadline of all the functions and test cases to Friday night(25/10). We make sure the pytests pass on Satursday and leave Sunday for more testing and writes the assurance.md and teamwork.md. 
We usually meet up when we have bugs in our code or we need some clarification which need to get the consensus of the whole group such as how database should be set up. For progress checkups, we use facebook messager to ask about how the project goes for everyone.
Since Owen has experienced on backend, he proofread our code to make sure there are no bugs. Anothy and Arprit works on the assurance.md since the concepts behind the assurance.md is relatively new and it takes time to understand. Ann is in charge of the teamwork.md. 

# What we have improved
In terms of communication, we make used of communication software instead of meetup. We talk to each other when we modified something from public files like server.py and database.py. Since we merge more often, we also proofread each others' code before we actually merge our code into master.

# Challenges that we faced as a team
## Time Limit
It is due in the midterm so some people might have several assignments due in the same week which leads to more intense pressure. It is also harder to meet up face-to-face since we have more engagements in other courses. 

## Implementing the database
Throughout the whole iteration 2, we made a lot of modification in the database. It is based on our 3 key components - user, channel and message. We are using class to structure our database whhich allow us to plan out the attribute and method. While we working on our parts, we add helper functions as class method which require us to communicate as a team more often since someone else might make the similar functions or it will cause merge conflict if we are not all aware of the changes.

## Connecting frontend and backend
(I didn't do anything for frontend. But i guess it breaks the functions that we have right now? Or found out that the format of returning output is wrong)

## Divided functions
The way that we divide the work make us to work with functions simultaneously. However, the functions are seldom having to wait til the previous function to be done. For example, almost all the functions need auth/register in order to check the token. Therefore, we would hardcode the related information in order to do testing.

# What we can improve next time
We can implement the function earlier.
We should test the frontend earlier.