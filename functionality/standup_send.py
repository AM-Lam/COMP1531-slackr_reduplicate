import jwt
from datetime import timedelta, datetime
from .database import (get_data, get_secret, get_channel, check_valid_token,
                       is_user_member)
from .access_error import AccessError, Value_Error


#   standup_send(token, channel_id, message);
#   return void
#   Exception: Value_Error when:
#       - Channel (based on ID) does not exist,
#       - Message is more than 1000 characters,
#   AccessError when :
#       - The authorised user is not a member of the channel that the message is within,
#       - If the standup time has stopped
#   Description: Sending a message to get buffered in the standup queue, assuming a standup is currently active

MESSAGE_STANDUP = ""

def standup_send(token, channel_id, message):
    # find u_id associated with token (with non-existent database)
    u_id = check_valid_token(token)

    if not is_user_member(u_id, channel_id):
        raise AccessError(description="You are not a member of this channel")

    check_message_length(message)
    check_valid_standup_time(channel_id)
    send_message(u_id, message)

    return


def check_message_length(message):
    if len(message) <= 1000:
        return True
    else:
        raise Value_Error(description="Message is too long.")


def check_valid_standup_time(channel_id):
    # for now I don't know about the channel class so I'm gonna pretend
    # if channel.standup_time < datetime.today
    # raise AccessError
    channel = get_channel(channel_id)

    channel_data = channel.get_channel_data()
    try:
        if datetime.now() > channel_data["standup"]:
            raise AccessError(description="The standup time has finished.")
        else:
            return True
    except TypeError:
        raise AccessError(description="The standup time has finished.")
    raise Value_Error(description="Channel does not exist or cannot be found.")


def send_message(u_id, message):
    # send a message corresponding to token in the channel_id
    global MESSAGE_STANDUP

    MESSAGE_STANDUP += str(u_id)
    MESSAGE_STANDUP += ": "
    MESSAGE_STANDUP += str(message)
