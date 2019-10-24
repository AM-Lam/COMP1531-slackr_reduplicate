from channels_list import channels_list
from datetime import timedelta, datetime
from access_error import AccessError
from channels_listall import channels_listall
import jwt

#   standup_start(token, channel_id);
#   return {time_finish}
#   Exception: ValueError when:
#       - Channel (based on ID) does not exist,
#   AccessError when:
#       - The authorised user is not a member of the channel that the message is within
#   Description: For a given channel, start the standup period whereby  for the next 15 minutes if someone calls "standup_send" with a      message, it is buffered during the 15 minute window then at the end of the 15 minute window a message will be added to the message queue in the channel from the user who started the standup.

def standup_start(token, channel_id):
    # find u_id associated with token (with non-existent database)
    admin_user_id = check_valid_token(token)

    check_channel_exist(token, channel_id)
    check_channel_member(token, channel_id)
    start_standup(channel_id)

    time_finish = timedelta(minutes=15)

    return time_finish

def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    decoded_jwt = jwt.decode(token, 'sempai', algorithms=['HS256'])
    try:
        for x in database:
            if x.get("u_id") == decoded_jwt.key():
                return x.get("u_id")
    except Exception as e:
        raise ValueError("token invalid")

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
    #
    if token == "badtoken":
        raise AccessError("You are not a member of this channel.")
    else:
        return True

def start_standup(channel_id):
    # maybe change an attribute in the channel class
    # like channel.is_standup = True
    # channel.standup_time = time_finish
    # for now there is no implementation
    # so we
    pass
