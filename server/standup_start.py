#   standup_start(token, channel_id);
#   return {time_finish}
#   Exception: ValueError when:
#       - Channel (based on ID) does not exist,
#   AccessError when:
#       - The authorised user is not a member of the channel that the         message is within
#   Description: For a given channel, start the standup period whereby  for the next 15 minutes if someone calls "standup_send" with a      message, it is buffered during the 15 minute window then at the end of the 15 minute window a message will be added to the message queue in the channel from the user who started the standup.

def standup_start(token, channel_id):
    time_finish = 0
    return time_finish
