import jwt
from datetime import timedelta, datetime
from .database import get_data, get_secret
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

    check_channel_exist(token, channel_id)
    check_channel_member(u_id, channel_id)
    check_message_length(message)
    check_valid_standup_time(channel_id)
    send_message(u_id, message)

    return

def check_valid_token(token):
    # find the user ID associated with this token, else raise a Value_Error
    DATABASE = get_data()
    SECRET = get_secret()
    token = jwt.decode(token, SECRET, algorithms=['HS256'])

    for x in DATABASE["users"]:
        user_id = x.get_u_id()
        if user_id == token["u_id"]:
            return user_id
    raise Value_Error(description="token invalid")


def check_channel_exist(token, channel_id):
    DATABASE = get_data()
    # check if channel_id exists, else raise a Value_Error

    for x in DATABASE["channels"]:
        if x.get_id() == channel_id:
            return True
    raise Value_Error(description="Channel does not exist or cannot be found.")


def check_channel_member(u_id, channel_id):
    # we need to find a way to know what members correspond to which channels, for now, pass
    DATABASE = get_data()

    for x in DATABASE["channels"]:
        if x.get_id() == channel_id:
            if u_id in x.get_members():
                return True
            else:
                raise AccessError(description="You are not a member of this channel.")
    raise Value_Error(description="Channel does not exist or cannot be found.")


def check_message_length(message):
    if len(message) <= 1000:
        return True
    else:
        raise Value_Error(description="Message is too long.")


def check_valid_standup_time(channel_id):
    # for now I don't know about the channel class so I'm gonna pretend
    # if channel.standup_time < datetime.today
    # raise AccessError
    DATABASE = get_data()

    for x in DATABASE["channels"]:
        if x.get_id() == channel_id:
            y = x.get_channel_data()
            try:
                if datetime.now() > y["standup"]:
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
