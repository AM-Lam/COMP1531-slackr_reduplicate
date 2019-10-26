from datetime import timedelta, datetime
from .access_error import AccessError
from .message_send import message_send
import jwt
import time

#   standup_start(token, channel_id);
#   return {time_finish}
#   Exception: ValueError when:
#       - Channel (based on ID) does not exist,
#   AccessError when:
#       - The authorised user is not a member of the channel that the message is within
#   Description: For a given channel, start the standup period whereby  for the next 15 minutes if someone calls "standup_send" with a message, it is buffered during the 15 minute window then at the end of the 15 minute window a message will be added to the message queue in the channel from the user who started the standup.

def standup_start(token, channel_id):
    # find u_id associated with token (with non-existent database)
    u_id = check_valid_token(token)

    check_channel_exist(channel_id)
    check_channel_member(u_id, channel_id)
    start_standup(channel_id)

    MESSAGE_STANDUP = ""

    time_current = datetime.now()
    time_finish = time_current + timedelta(minutes=15)

    end_standup(token, channel_id)

    return time_finish

def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    global DATABASE
    global SECRET

    token = jwt.decode(token, SECRET, algorithms=['HS256'])

    try:
        for x in DATABASE["users"]:
            y = x.get_user_data()
            if y.get("u_id") == token["u_id"]:
                return y.get("u_id")
    except Exception as e:
        raise ValueError("token invalid")

def check_channel_exist(channel_id):
    global DATABASE
    # check if channel_id exists, else raise a ValueError

    for x in DATABASE("channels"):
        if x.get("channel_id") == channel_id:
            return True
    raise ValueError("Channel does not exist or cannot be found.")

def check_channel_member(u_id, channel_id):
    # we need to find a way to know what members correspond to which channels, for now, pass
    global DATABASE

    for x in DATABASE("channels"):
        if x.get("channel_id") == channel_id:
            channel_dictionary = x.get_channel_data()
            member_list = channel_dictionary["members"]
            if u_id in member_list:
                return True
            else:
                raise AccessError("You are not a member of this channel.")
    raise ValueError("Channel does not exist or cannot be found.")

def start_standup(channel_id):
    # give a timedate object to the database
    global DATABASE
    
    time_current = datetime.now()
    time_finish = time_current + timedelta(minutes=15)

    for x in DATABASE("channels"):
        if x.get("channel_id") == channel_id:
            DATABASE.update_user_data({"standup": time_finish})
    raise ValueError("Channel does not exist or cannot be found.")

def end_standup(token, channel_id):
    global DATABASE
    global MESSAGE_STANDUP

    time_current = datetime.now()
    time_finish = time_current + timedelta(minutes=15)

    while datetime.now() <= time_finish:
        time.sleep(1)

    message_send(token, channel_id, MESSAGE_STANDUP)
