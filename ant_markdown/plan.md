plan.md
=======

_Write a brief 1-page plan highlighting how you will approach the following iteration (the development stage)._

_Since iteration 2 is about implementing the interface that has been provided to you already by Sally and Bob, you should be able to make enough sense of the requirements to_
 1) _Estimate the time they take,_
 2) _Break them up into logical buckets,_
 3) _Figure out the order in which you would implement them_

_This isn't meant to be overly complicated. It's just to demonstrate that you've had a *thoughtful* guess at how you'd go about developing the functions._

_You may include diagrams, tables or whatever other information you believe conveys your plan._

___

Before we approach any of these functions, we would like to have a quick standup where we divide the 32 functions between the 4 of us, and from this we would co-ordinate and push our functions to our own branches.

After this, I will take an extensive look at the specifications given by the front_end team for my specific functions, including what I should return if there is an Exception. This will likely take up the bulk of the tests. As for other tests, I would plan to have successful tests, and tests if certain variables are invalid. I doubt we will have many edge cases, but if we do we'll try to address them as they occur.

EDIT: I have looked at my own functions and have thought of them as such:

user_profile_setname(token, name_first, name_last)
	1. I estimate this function in its entirety would take 1 hour.
	2. Check if token is valid
	   Check if first name is valid
	   Check if last name is valid
	   Assign new names to profile

user_profile_setemail(token, email)
	1. I estimate this function in its entirety would take 1 hour.
	2. Check if token is valid
	   Check if email is valid
	   Check if email is being used
	   Assign new email to profile

user_profile_sethandle(token, handle_str)
	1. I estimate this function in its entirety would take 1 hour.
	2. Check if token is valid
	   Check if handle is valid
	   Assign new email to profile

user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, 	y_end)
	1. With the image url management the longest this could take to implement is 2 hours.
	2. Check if token is valid
	   Check if img_url is valid
	   Check if x coords are valid
	   Check if y coords are valid
	   Pass coords, img_url to profile

standup_start(token, channel_id); return {time_finish}
	1. I think this function would take a maximum of 2 hours.
	2. Check if token is valid
	   Check if channel is valid
	   Check if user can access channel
	   Engage standup buffer
	   Hold for standup_send

standup_send(token, channel_id, message)
	1. I think this function would take a maximum of 2 hours.
	2. Check if token is valid
	   Check if channel is valid
	   Check if user can access channel
	   Check if standup time is active
	   Check is message isn't too long
	   Post message to channel
	   Send message to standup queue

search(token, query_str)
	1. This function should take 2 hours.
	2. Check if token is valid
	   Search message database
	   Identify matches (binary search)
	   Return message list

admin_userpermission_change(token, u_id, permission_id)
	1. This function should take 3 hours.
	2. Check if token is valid
	   Check if the user is valid
	   Check if the permission given is a valid permission
	   Check if the calling user is an owner or an admin
	   Change the user's permission
	   Return
