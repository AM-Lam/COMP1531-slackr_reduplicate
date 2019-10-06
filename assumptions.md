- General Assumptions
  - assume we have the necessary funds/space/resources to host our backend.

---

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
