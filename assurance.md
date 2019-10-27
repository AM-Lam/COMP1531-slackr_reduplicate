## Assurance.md ##

## W17A-Dead_Thunder_Squirrels ##






_TABLE OF CONTENTS

Section                        
Page
SECTION 1.  SOFTWARE DESCRIPTION------------------------------------------------------------2

1.1      Scope

1.2      Frontend

1.3      Uses

SECTION 2.  ROLES AND RESPONSIBILITIES-----------------------------------------------------2

2.1      Organization

2.2      Work division

2.2.1       Checklists

SECTION 3.  SQA REQUIREMENTS-------------------------------------------------------------------3

3.1      Task:  Requirements phase

3.2      Task:  Design phase

3.3      Task:  Implementation phase

3.4      Task:  Testing phase

SECTION 4.  ER Diagrams---------------------------------------------------------------------------------4_




1.0 SOFTWARE DESCRIPTION
This backend software package was created in compliance with the frontend software package developed by BananaPie Pty Ltd and follows the specifications provided by Rayden Pty Ltd who have been constantly updating the specs as per UNSW. This software is being developed to be used by the educational institution UNSW. It will be a means for students and staff of UNSW to communicate with each other.
The backend created by us is split into thirty two different functions. Each function has been documented and testing files have been created for each function. The development of this software shall be based on the functionality of the software packages provided by BananaPie Pty Ltd.

2.0 ROLES AND RESPONSIBILITIES
To work towards the completion of the backend software package, and to provide the software quality assurance, many steps have been taken. The project was divided into 32 different functions and the work was split equally amongst four engineers working on the backend. Each engineer was initially required to set up files for their functions and was made to create rigorous tests that would make sure the software would comply to the users needs and specifications. Once the tests were written, each engineer was tasked with implementing the functionality of the tests they wrote. The database was created by the whole team so everyone could have a preferred data structure. Checklists with the high level requirements were created for each member of the team. A checklist was created for the function implementation and its endpoints. Another was created for the testing phase.
 

72648378_1001840013514004_885153550949154816_n.jpg

73097444_539177293539226_4111722662345048064_n.png


3.0 SOFTWARE QUALITY ASSURANCE REQUIREMENTS

3.1 REQUIREMENTS PHASE
In this phase of the project our team got together and we did a detailed requirements analysis. Initially many assumptions were made on the specifications which were well documented. This helped in getting confirmation from the stakeholders that we were representing the requirements correctly. User stories were created to get a better perspective of what the stakeholders actually wanted. Once the user stories were made our team assigned each story, story points based on its complexity.  

3.2 DESIGN PHASE
In this phase we had to design the basic layout for all our functions, so our functions could easily be called by others working on the project. The initial steps that had to be taken was building a database where all the information from all the functions could be stored. Coming up with a good design for the database was a very important part of the design phase as all thirty two are interlinked by the database. To reach a final design, our team had to get together and we started by making some rough sketches. After the initial structure was made, many small changes and modifications were made and pushed through gitlab. 

3.3 IMPLEMENTATION PHASE
For this part of the software development lifecycle(iteration 2), the implementation for each function was completed. Each function was well documented with many comments in the code. To make sure that the implementation was proceeding down the right path, our team set a criteria to make sure all the pytests worked.
Tools like Python3-coverage were used as a benchmark to make sure that every line of our code was being tested for achieving the perfect functionality. Using this tool helped us create more tests ensuring smooth functionality from the backend.

3.4 TEST PHASE
We have implemented numerous checks and balances to make sure that our backend functions without errors, and that it returns the correct output for the frontend. For each function there is a corresponding _test file that runs a series of unit tests. These unit tests test for correct input, as well as appropriate responses for issues such as ValueErrors or AccessErrors. These unit tests are available to our client if they wish to verify as such.
To make sure that our unit tests tested the majority of their function for defects, we also ran a code coverage test with coverage.py, and used the generated html report to write more intensive tests.
Other tools like pylint and postman were also used for ensuring that the software quality was excellent and the backend works to comply with the frontend 


4.0 ENTITY-RELATIONSHIP DIAGRAMS



74471414_397445917875117_4291649867555536896_n.png

As a part of our design phase, we looked to visually link our functions to our objects via an entity-relationship diagram. The diagram shown above allowed us to understand the relationships between our team’s functions, even while we generally separated our functions by 8 each.  Most of these functions, as can be seen, only change one value (similar relationships have been clustered) such as the functions for updating string values in the profile. Another example, many functions that involve messages usually also have to configure with the channel the message is based in, usually through calls to database.

Whilst each function has its own complexities, this diagram is able to show that it can be split up into relatively stand-alone problems.


