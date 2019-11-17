"""
Functions that relate to standup functionality.
"""

from datetime import datetime, timedelta
from threading import Timer
from .message import send_message
from .database import (get_channel, check_valid_token, is_user_member,
                       get_user, Messages)
from .access_error import AccessError, Value_Error


def standup_end(channel):
    """
    Set the standup to inactive and send the messages that were sent
    during the standup to the channel.
    """
    print("Standup just ended")

    standup_data = channel.get_standup()

    start_user = standup_data["start_user"]
    message_text = standup_data["messages"]

    m_id = channel.get_m_id()
    channel.increment_m_id()

    standup_message = Messages(m_id, start_user.get_u_id(), message_text,
                               channel.get_id(), datetime.now(), [])

    send_message(channel, standup_message, datetime.now())

    # now reset the channel standup data
    channel.set_standup({
        "time_finish" : None,
        "is_active" : False,
        "messages" : "",
        "start_user" : None
    })



def standup_start(token, channel_id, length):
    """
    standup_start(token, channel_id, length);
    return {time_finish}
    Exception: Value_Error when:
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
    channel = get_channel(channel_id)

    # if the user is not a member of this channel, raise an AccessError
    if not is_user_member(u_id, channel_id):
        raise AccessError(description="You are not a member of this channel.")

    # check if there is an active standup session
    if channel.get_standup()["is_active"]:
        raise Value_Error(description="There is already an active standup.")

    # set the standup end time to be X amount of time from now
    time_finish = datetime.now() + timedelta(seconds=length)

    # give the channel this new standup time
    channel.set_standup({
        "time_finish" : time_finish,
        "is_active" : True,
        "messages" : "",
        "start_user" : get_user(u_id)
    })

    # start a timer to end the standup after length seconds have elapsed
    Timer(length, standup_end, args=(channel,)).start()

    # return the finish time for the standup
    return {"time_finish": time_finish.timestamp()}

######################################################################################

def standup_send(token, channel_id, message):
    """
    standup_send(token, channel_id, message);
    return {}
    Exception: Value_Error when:
        - Channel (based on ID) does not exist,
        - Message is more than 1000 characters,
    AccessError when:
        - The authorised user is not a member of the channel that the
          message is within,
        - If the standup time has stopped
    Description: Sending a message to get buffered in the standup queue
    assuming a standup is currently active
    """

    # check if the token is valid and decode it
    u_id = check_valid_token(token)
    user = get_user(u_id)

    # check if the channel exists
    channel = get_channel(channel_id)

    # if the user is not a member of this channel, raise an AccessError
    if not is_user_member(u_id, channel_id):
        raise AccessError(description="You are not a member of this channel.")

    # check if there is an active standup session
    if not channel.get_standup()["is_active"]:
        raise AccessError(description="There are no active standups.")

    # check if the message meets length requirements
    if len(message) > 1000:
        raise Value_Error(description="Message is too long.")

    # append the message to the standup message variable
    channel.get_standup()["messages"] += f'{user.get_handle()}: {message}\n'

    return {}


def standup_active(token, channel_id):
    """
    standup/active(token, channel_id);
    return { is_active, time_finish }
    Exception: Value_Error when:
        - Channel ID is not a valid channel
    Description: For a given channel, return whether a standup is
    active in it, and what time the standup finishes. If no standup is
    active, then time_finish returns None
    """

    # check if the token is valid and get the channel object we need
    check_valid_token(token)
    channel = get_channel(channel_id)

    # format the datetime object in a way JS can understand if it is
    # active
    time_finish = channel.get_standup()["time_finish"]
    if time_finish is not None:
        time_finish = time_finish.timestamp()

    status = {
        "time_finish": time_finish,
        "is_active": channel.get_standup()["is_active"]
    }

    return status
