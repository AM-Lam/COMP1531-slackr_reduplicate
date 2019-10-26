import jwt
import threading
from datetime import datetime
from .access_error import *
from .database import *


def send_message(channel, message, time_sent):
    # wait until we have passed beyond the desired time to send the message
    while datetime.utcnow() < time_sent:
        continue
    
    # now just append the message we created earlier to the provided channel
    channel._messages.append(message)


def message_sendlater(token, channel_id, message, time_sent):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, True):
        raise AccessError(description="This token is invalid")

    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # first deal with an easy to catch error, is the message too large to send
    if len(message) > 1000:
        raise ValueError(description="Messages must be below 1000 characters")
    
    # next error, check the current date against time_sent and raise an
    # exception if time_sent is in the past
    if datetime.utcnow() > time_sent:
        raise ValueError(description="Cannot send messages in the past")
        
    # ensure that the channel we are trying to send a message to actually exists
    # and that we are an authorised user in it (which I take here to mean a
    # member of the channel)
    channel_ = None
    for channel in server_data["channels"]:
        if channel_id == channel._channel_id:
            channel_ = channel
            break
    
    if channel_ is None:
        raise ValueError(description="Channel does not exist")
    
    if u_id not in channel_._members:
        raise AccessError(description="You cannot send messages in this channel")
    
    # now create the message we will be sending
    to_send = Messages(len(channel_._messages) + 1, u_id, message, channel_id,
                       time_sent, [])
    
    # start a thread that will call send_message
    threading.Thread(target=send_message, args=(channel_, message, time_sent)).start()
    
    return {}

