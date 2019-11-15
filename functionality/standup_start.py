import jwt
import time
from datetime import timedelta, datetime
from .message import message_send
from .database import (get_data, get_secret, check_valid_token, is_user_member,
                       get_channel)
from .access_error import AccessError, Value_Error


#   standup_start(token, channel_id);
#   return {time_finish}
#   Exception: Value_Error when:
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

    is_user_member(u_id, channel_id)
    start_standup(channel_id)

    time_current = datetime.now()

    if DEV:
        time_finish = time_current + timedelta(seconds=5)
    else:
        time_finish = time_current + timedelta(minutes=15)

    end_standup(token, channel_id, time_finish)

    return time_finish


def start_standup(channel_id):
    # give a timedate object to the database
    DATABASE = get_data()
    
    time_current = datetime.now()
    time_finish = time_current + timedelta(minutes=15)

    channel = get_channel(channel_id)
    channel.set_standup(time_finish)
    
    if not channel:
        raise Value_Error(description="Channel does not exist or cannot be found.")


def end_standup(token, channel_id, time_finish):
    global MESSAGE_STANDUP
    DATABASE = get_data()

    while datetime.now() <= time_finish:
        time.sleep(1)

    channel = get_channel(channel_id)
    channel.set_standup(None)

    message_send(token, channel_id, MESSAGE_STANDUP)
