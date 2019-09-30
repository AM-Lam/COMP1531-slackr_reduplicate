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

I am taking the functions:

	user_profile_setname(token, name_first, name_last); return void
	Exception: ValueError when: name_first is more than 50 characters, 	name_last is more than 50 characters
	Description: Update the authorised user's first and last name

	user_profile_setemail(token, email); return void
	Exception: ValueError when: Email entered is not a valid email, Email 	address is already being used by another user
	Description: Update the authorised user's email address

	user_profile_sethandle(token, handle_str); return void
	Exception: ValueError when:handle_str is no more than 20 characters
	Description: Update the authorised user's handle (i.e. display name)

	user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, 	y_end); return void
	Exception: ValueError when: img_url is returns an HTTP status other 	than 200, x_start, y_start, x_end, y_end are all within the 		dimensions of the image at the URL.
	Description: Given a URL of an image on the internet, crops the image 	within bounds (x_start, y_start) and (x_end, y_end). Position (0,0) 	is the top left.

	standup_start(token, channel_id); return {time_finish}
	Exception: ValueError when:Channel (based on ID) does not exist, 	AccessError whenThe authorised user is not a member of the channel 	that the message is within
	Description: For a given channel, start the standup period whereby 	for the next 15 minutes if someone calls "standup_send" with a 		message, it is buffered during the 15 minute window then at the end 	of the 15 minute window a message will be added to the message queue 	in the channel from the user who started the standup.

	standup_send(token, channel_id, message); return void
	Exception: ValueError when: Channel (based on ID) does not exist, 	Message is more than 1000 characters, AccessError when The authorised 	user is not a member of the channel that the message is within, If 	the standup time has stopped
	Description: Sending a message to get buffered in the standup queue, 	assuming a standup is currently active

	search(token, query_str); return {messages}
	Exception: N/A
	Description: Given a query string, return a collection of messages 	that match the query

	admin_userpermission_change(token, u_id, permission_id); return void
	Exception: ValueError when: u_id does not refer to a valid user, 	permission_id does not refer to a value permission, AccessError 	when The authorised user is not an admin or owner
	Description: Given a User by their user ID, set their permissions to 	new permissions described by permission_id