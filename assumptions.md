<<<<<<< assumptions.md
=======
- General Assumptions
  - assume we have the necessary funds/space/resources to host our backend.
  - assuming  slackr is a platform to improve communciation between stakeholders in the university course. Therefore, professors, tutors and students will use slackr to communicate especially when the course will involve teamwork. In this way, we won't have to use our personal account to communciate and can make sure students that are in a team would be able to get a hold with each others.
  - assume all the given token is valid and is a member of at least one channel
  - assume owner of the channel is also an admin of that channel.
  - assume user can join multiple channels.
  - assume a user can be admin in just one channel or multiple channels.
  - assume admin in one channel don't have the same permission in other channels unless they are also an admin in those channels.
  - assume when the user register, first name of the user is the username since there are no username in register function.
  - assume permission of anyonewho joins the channel is default as 'member' except the owner unless channel\_addowner, admin\_userpermission_change is implemented.
  - assume Admin of the slackr is also an admin of any channel under slackr if such a role exists. Same applied to owner.
  - assume all the id is unique among slackr. For example, the same number won't be generated in the same list even if the same type of function is executed. For example same message is generated in different channels the message\_id will be different and will only be used in the original post. There are no duplicate message\_ids in the same list.
  - assume the same id number can appear in different type of id such as '1' can be a channel\_id and also a u\_id.

- Structure of the database(dictionary/list that I use to store the data):
  - assume all types of ID (eg. u\_id, message\_id, react\_id) are generated and stored in a database in a form of dictionaries or lists if the related function is successfully executed.
    # Record of all successful register user
  - u\_id\_list:{token: u_id}
  - u\_id\_dic:{u\_id: {email, first name, last name, handle}}
    # message\_id\_list = {message_id: message}
  - message\_id\_dic: {message\_id: {token, channel\_id}}
  - permission\_id\_list: {1, 2, 3} # permission: 'owner', 'admin', 'member'
    #Based on different channels user have different permission
  - permission\_id\_dic = {token: {channel\_id: permission\_id}}
    # keep track of the existing channels in the slackr
  - channel\_id\_dic: {channel\_id: channel name} # eg.{1: channel1, 2: channel2,...}
    # keep track of the valid react that can be used in the slackr
  - react\_type\_list: {react\_id: reaction} # eg. reaction: like,love, smile}
  - format of react\_id\_dic: message\_id: {token, messsage\_id, react\_id}
  - pinned\_list: {message_id: token}
---

- message_send:
  - Author: Lai Ming(Ann) Lam
  - assume the message contains any type of characters like space, upper or lower cases, numbers, or ,./<>;':"()_*&^%$#@!~`-+=. 
  - assume characters which excluded in ASCII table cannot be sent such as emoji.

- message_remove:
  - Author: Lai Ming(Ann) Lam
  - assume the poster of that message and admin of that channel has the permission to remove messages.
  - assume if the message no long existed means that the message_id is deleted or cannot be found.
  - assume all the message\_id is stored in a dictionary called message\_id\_dic and token and channel\_id is stored in the key.
  - assume channel_list can be used to check whether the user is existing in the channel.

- message_edit:
  - Author: Lai Ming(Ann) Lam
  - assume the poster of that message is the only can edit the message even admin and owner cannot edit the message.
  - assume authorised user is the one having a valid account in slackr

- message\_react and message\_unreact(applied for both):
  - Author: Lai Ming(Ann) Lam
  - assume the poster of that message is the only can react or unreact the message even admin and owner cannot (un)react the message.
  - assume the poster can react on their own posts.
  - assume react\_id is represented by a react\_type\_list to check which reaction to pick. 

- message\_pin and message\_unpin (applied for both):
  - Author: Lai Ming(Ann) Lam
  - assume admin can pin on any message that they see
  - assume every member in the channel can see what message is (un)pinned.
  - assume only admin of the channel have the permission to pin or unpin the message.
  - assume more than one messages can be (un)pin.

- user_profile:
  - Author: Lai Ming(Ann) Lam
  - assume handle means that the username of the user.

- channel_leave assumptions
  - Author: Owen Chandler
  - assuming that if a user is not a part of a channel that the functions fails with no message/exception

- channel_addowner assumptions
  - Author: Owen Chandler
  - assume that if a user owns a channel then they are a part of it

- channel_removeowner assumptions
  - Author: Owen Chandler
  - assume that an owner CAN remove themselves as an owner of a channel

- channel_join assumptions
  - Author: Owen Chandler
  - assume that trying to join a non-existent channel will not raise any exceptions and fail quietely

- channels_listall assumptiosn
  - Author: Owen Chandler
  - assume that listall means listall, including private channels

- channels_create assumptions
  - Author: Owen Chandler
  - assume that two, or more, channels can have the same name
  - assume that a user doesn't need any special permissions to create a channel (we can easily fix 
    this later if untrue)

- message_sendlater assumptions
  - Author: Owen Chandler
  - assume that time_sent is a datetime object
  - assume that time_sent is in the same timezone as the server
  - assume that authorised_user refers to a user that is a member of the channel
  - at this point rather than delaying sending the message to the server (which would likely require
    concurrency to avoid slowing everything down) we will just send the message with the set time
    and assume that messages will only be shown on the client at and after the time of creation has
    passed

- auth_register:
  - Author: Arpit Rulania
  - calling auth_register automatically logs in the user for the current session.
  - z1111@unsw.com is equal to z1111@student.unsw.com
  - user@gmail.com is equal to user@gmail.com.au 
  - unsuccessful register returns an empty dictionary
  - if email on server is z11111@student.unse.edu.au and
    a new registeration z11111@unse.edu.au should not be possible
  - auth_register.validate_regEmail returns true if email does not exist

- auth_login:
  - Author: Arpit Rulania
  - unsuccessful login returns an empty dictionary
  - password field or email field left empty should raise an error
  - raise error if password is incorrectly matched to the email
  - auth_login.validate_email returns true if email does exist on the server

- auth_logout:
  - Author: Arpit Rulania
  - logout should not be possible twice        
  - logout returns value errors for invalid tokens
  - logout returns true boolean on sauccessful logout

- auth_passwordreset_request:
  - Author: Arpit Rulania
  - the reset code is temporarily saved in the server for a short time

- auth_passwordreset_reset:
  - Author: Arpit Rulania
  - the reset code must be an integer without any alphabets or special characters
  - the new password should follow valid password rules
  - the new password should not be same as the old password

- channel_invite:
  - Author: Arpit Rulania
  - only the owners of the channel can invite other users
  - invited user when added to the channel is not given special permissions
  - user is added as a member imediatly after detail verification

- channel_details:
  - Author: Arpit Rulania
  - all_members lists also includes owner_members
  - if only one member then both lists, all_members and owner_members are 
    same

- channel_messages:
  - Author: Arpit Rulania
  - if there are 10 messages and start is 10 then start = end = -1
  - function should not uotput the same message more than once(i.e. filter 
    out the duplicate messages)

- user_profile_setname assumptions
  - Author: Anthony Wallace
  - assume that inputs given by users are reasonable and will not cause edge cases. 
  - We will assume that only alphanumeric characters are used. 

- User_profile_setemail:
  - Author: Anthony Wallace
  - assume inputs are reasonable, ie they are email strings
  - assume that email addresses are exclusive to each user

- user_profile_sethandle:
  - Author: Anthony Wallace
  - assume that inputs do not include exclusively white space, 
  - that inputs comply with the Unicode Standard, 
  - that inputs do not include formatting characters like zero width spaces. You would want to customise your handle to a larger extent than your name.

- user_profiles_setphoto:
  - Author: Anthony Wallace
  - assuming that the given URL actually redirects to a valid image format (png, jpg). 
  - This image format will not be a gif, bmp, or other hard to integrate format. We will also 
  - assume that given URLs are not potentially malicious to our backend. 
  - Though this is more a social issue, we would like to assume given images are appropriate for a University program.

- standup_start:
  - Author: Anthony Wallace
  - assume that standups can not overlap over one another
  - assume that time_finish is a datetime object
  - assume that time_finish is in the same timezone as server
  - assume standup_start is NOT responsible for returning standup messages after 15 minutes
  - assume standup_start responsible only for starting timer
  
- standup_send:
  - Author: Anthony Wallace
  - We will assume that messages sent can be displayed as a message, i.e. Unicode Standard, no formatting characters
  - assume that time_finish is a datetime object
  - assume that time_finish is in the same timezone as server

- search:
  - Author: Anthony Wallace
  - Assume the Unicode Standard
  - assume that messages are catalogued in chronological order
  - assume that search returns both full matches and partial matches eg 'set' = ["setQuery"]

admin_userpermission_change:
  - Author: Anthony Wallace
  - assume that there is no other way to access the database for a non admin/owner.
  - assume admin and owner have different permission levels
>>>>>>> assumptions.md
