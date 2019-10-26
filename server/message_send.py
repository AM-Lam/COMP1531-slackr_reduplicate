import jwt
import threading
from .database import *
from datetime import datetime 
from .access_error import *

def message_send(token, channel_id, message):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, True):
        raise AccessError(description="This token is invalid")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]
    
    # Message is more than 1000 characters
    if len(message) > 1000:
        raise ValueError(description="Messages must be less than 1000 characters")

    channel_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        if channel.get_id() == channel_id:
            channel_ = channel
            break
    
    if channel_ is None:
        raise ValueError(description="Channel does not exist")

    if u_id not in channel_.get_members():
        raise AccessError(description="You don't have access in this channel")
        
    # now create the message we will be sending
    message_id = channel_.get_m_id()
    to_send = Messages(message_id, u_id, message, channel_id,
                       datetime.utcnow(), [])
    
    # increment the channel's max message id
    channel_.increment_message_id()
    
    # start a thread that will call send_message
    channel_.add_message(to_send)

    # return the new message's id
    return { "message_id" : message_id }

