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

- message_sendlater assumptions
  - Author: Owen Chandler
  - assume that time_sent is a datetime object
  - assume that time_sent is in the same timezone as the server
  - assume that authorised_user refers to a user that is a member of the channel
  - at this point rather than delaying sending the message to the server (which would likely require
    concurrency to avoid slowing everything down) we will just send the message with the set time
    and assume that messages will only be shown on the client at and after the time of creation has
    passed
