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

