"""
Functions that relate to standup functionality.
"""

import jwt
import time
from datetime import *
from .message import *
from .database import *
from .access_error import *

MESSAGE_STANDUP = ""

def standup_start(token, channel_id, length):
    """
    standup_start(token, channel_id, length);
    return {time_finish}
    Exception: ValueError when:
        - Channel (based on ID) does not exist,
        - An active standup is currently running in this channel
    AccessError when:
        - The authorised user is not a member of the channel that the message is within
    Description: For a given channel, start the standup period whereby  for the
    next 15 minutes if someone calls "standup_send" with a message, it is buffered
    during the 15 minute window then at the end of the 15 minute window a message
    will be added to the message queue in the channel from the user who started the
    standup.
    """

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # check if the channel exists
    get_channel(channel_id)

    # if the user is not a member of this channel, raise an AccessError
    if not is_user_member(u_id, channel_id):
        raise AccessError(description="You are not a member of this channel.")

    # check if there is an active standup session
    if get_channel(channel_id).get_standup() != None:
        raise AccessError(description="There is already an active standup.")

    # set the standup end time to be X amount of time from now
    time_finish = datetime.now() + timedelta(seconds=length)

    # give the channel this new standup time
    get_channel(channel_id).set_standup(time_finish)

    # TODO: check the functionality of the below code
    # wait until the standup finishes, then send the message
    while datetime.now() <= time_finish:
        time.sleep(1)
    get_channel(channel_id).set_standup(None)
    message_send(token, channel_id, MESSAGE_STANDUP)

    # return the finish time for the standup
    return time_finish

######################################################################################

def standup_send(token, channel_id, message):
    """
    standup_send(token, channel_id, message);
    return {}
    Exception: ValueError when:
        - Channel (based on ID) does not exist,
        - Message is more than 1000 characters,
    AccessError when:
        - The authorised user is not a member of the channel that the message is within,
        - If the standup time has stopped
    Description: Sending a message to get buffered in the standup queue, assuming a standup is currently active
    """

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # check if the channel exists
    get_channel(channel_id)

    # if the user is not a member of this channel, raise an AccessError
    if not is_user_member(u_id, channel_id):
        raise AccessError(description="You are not a member of this channel.")

    # check if the message meets length requirements
    if len(message) > 1000:
        raise ValueError(description="Message is too long.")

    # check if there is an active standup session
    if get_channel(channel_id).get_standup() == None:
        raise AccessError(description="There are no active standups.")

    # TODO: check if this works
    MESSAGE_STANDUP += str(u_id), ": ", str(message)

    return {}

def standup_active(token, channel_id):
    """
    standup/active(token, channel_id);
    return { is_active, time_finish }
    Exception: ValueError when:
        - Channel ID is not a valid channel
    Description: For a given channel, return whether a standup is active in it, and what time the standup finishes. If no standup is active, then time_finish returns None
    """

    dict = {"is_active" : None, "time_finish" : None}

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    dict["time_finish"] = get_channel(channel_id).get_standup()

    # check if there is an active standup session
    if get_channel(channel_id).get_standup() != None:
        dict["is_active"] = True
    else:
        dict["is_active"] = False

    return dict
