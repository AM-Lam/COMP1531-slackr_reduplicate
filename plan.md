For the second stage of the iteration there are a number of things that we should do in order to complete it properly and on-time. The first step in this is to break the requirements and functionality of the software into logical, modular chunks so that it is easy to work on different parts individually and see how they interact with each other. This division can be seen below:

![Image Link](https://drive.google.com/file/d/1NcTMOHCe8yb9xuoGI-xHfopTRRJ1KgG8/view?usp=sharing "Modules Diagram")

Each of the functions that are needed fits into one of these modules.

As for a timetable there are a few questions that we need to answer. First, what order should we complete the functions in? And second, how long will each module take to complete? 

For the first question, there are two options, we could either work on each section sequentially and only move onto a new one after completing the current one or we could work on the modules in parallel. The latter option is likely better, especially as we have already completed function stubs, and will significantly cut down on development time.

As for the second question, estimating the exact time of development for each module is frankly impossible. However, we can make a guess. Each individual function will likely take a few hours to complete, the more complex ones (message_sendlater and the standup functions for example) will likely take longer. The fact that we have already completed function stubs in iteration 1 will reduce the overall time however interacting with a server and database will probably take up the majority of our time.

So, taking both of these factors into account, we can estimate the overall time working on functions as around 12 hours each. However, we need to take into account the added time that unforeseen complications and, of course, bugs will take. We will also need to have thrice-weekly standup meetings at about 15-20 minutes each meeting to allow us to sort out problems face-to-face. So in actuality this iteration will probably take at least 20 hours of work per-person. 

Finally we need to consider the technology that we will be using to help us develop this iteration of the program. Clearly we will continue to use git and access it through gitlab. There are several benefits to this: first, git provides a VCS that will ensure that we can keep track of all our changes easily and secondly, Gitlab’s issues board will allow us to keep track of user stories and respond to changing requirements. We will also make use of coverage.py and pytest in order to organise the testing of our system and verify that it meets at least basic requirements.

