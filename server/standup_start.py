import jwt
import time
from datetime import timedelta, datetime
from .access_error import *
from .message_send import message_send
from .database import *


#   standup_start(token, channel_id);
#   return {time_finish}
#   Exception: ValueError when:
#       - Channel (based on ID) does not exist,
#   AccessError when:
#       - The authorised user is not a member of the channel that the message is within
#   Description: For a given channel, start the standup period whereby  for the 
#   next 15 minutes if someone calls "standup_send" with a message, it is buffered 
#   during the 15 minute window then at the end of the 15 minute window a message 
#   will be added to the message queue in the channel from the user who started the
#   standup.

MESSAGE_STANDUP = ""

def standup_start(token, channel_id):
    global MESSAGE_STANDUP
    
    # if this flag is true standups only take 5 seconds
    DEV = True
    
    # find u_id associated with token (with non-existent database)
    u_id = check_valid_token(token)

    MESSAGE_STANDUP = ""

    check_channel_exist(channel_id)
    check_channel_member(u_id, channel_id)
    start_standup(channel_id)

    time_current = datetime.now()

    if DEV:
        time_finish = time_current + timedelta(seconds=5)
    else:
        time_finish = time_current + timedelta(minutes=15)

    end_standup(token, channel_id, time_finish)

    return time_finish

def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    DATABASE = get_data()
    SECRET = get_secret()
    token_payload = jwt.decode(token, SECRET, algorithms=['HS256'])

    for x in DATABASE["users"]:
        user_id = x.get_u_id()
        if user_id == token_payload["u_id"]:
            return user_id
    raise ValueError(description="token invalid")

def check_channel_exist(channel_id):
    # check if channel_id exists, else raise a ValueError
    DATABASE = get_data()

    for x in DATABASE["channels"]:
        if x.get_id() == channel_id:
            return True
    
    raise ValueError(description="Channel does not exist or cannot be found.")

def check_channel_member(u_id, channel_id):
    # we need to find a way to know what members correspond to which channels, for now, pass
    DATABASE = get_data()

    for x in DATABASE["channels"]:
        if x.get_id() == channel_id:
            if u_id in x.get_members():
                return True
            else:
                raise AccessError(description="You are not a member of this channel.")
    
    raise ValueError(description="Channel does not exist or cannot be found.")

def start_standup(channel_id):
    # give a timedate object to the database
    DATABASE = get_data()
    
    time_current = datetime.now()
    time_finish = time_current + timedelta(minutes=15)
    found_channel = False
    for x in DATABASE["channels"]:
        if x.get_id() == channel_id:
            x.set_standup(time_finish)
            found_channel = True
            break
    
    if not found_channel:
        raise ValueError(description="Channel does not exist or cannot be found.")

def end_standup(token, channel_id, time_finish):
    global MESSAGE_STANDUP
    DATABASE = get_data()

    while datetime.now() <= time_finish:
        time.sleep(1)

    for x in DATABASE["channels"]:
        if x.get_id() == channel_id:
            x.set_standup(None)
            break

    message_send(token, channel_id, MESSAGE_STANDUP)
