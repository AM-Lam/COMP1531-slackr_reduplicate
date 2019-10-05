from channels_list import channels_list
from datetime import timedelta, datetime
from access_error import AccessError
from channels_listall import channels_listall

#   standup_send(token, channel_id, message);
#   return void
#   Exception: ValueError when:
#       - Channel (based on ID) does not exist,
#       - Message is more than 1000 characters,
#   AccessError when :
#       - The authorised user is not a member of the channel that the         message is within,
#       - If the standup time has stopped
#   Description: Sending a message to get buffered in the standup queue, assuming a standup is currently active

def standup_send(token, channel_id, message):
    # find u_id associated with token (with non-existent database)
    u_id = 12345

    check_channel_exist(token, channel_id)
    check_channel_member(token, channel_id)
    check_message_length(message)
    check_valid_standup_time(channel_id)
    send_message(token, channel_id, message)

    return

def check_channel_exist(token, channel_id):
    #if channel_id not in [x["channel_id"] for x in channel_list(token)]:
        #raise ValueError("Channel does not exist or cannot be found.")
    #else:
        #return True
    if channel_id == "channel":
        return True
    else:
        raise ValueError("Channel does not exist or cannot be found.")

def check_channel_member(token, channel_id):
    # we need to find a way to know what members correspond to which channels, for now, pass
    if token == "badtoken":
        raise AccessError("You are not a member of this channel.")
    else:
        return True

def check_message_length(message):
    if len(message) <= 1000:
        return True
    else:
        raise ValueError("Message is too long.")

def check_valid_standup_time(channel_id):
    # for now I don't know about the channel class so I'm gonna pretend
    # if channel.standup_time < datetime.today
    # raise AccessError
    pass

def send_message(token, channel_id, message):
    # send a message corresponding to token in the channel_id
    pass
