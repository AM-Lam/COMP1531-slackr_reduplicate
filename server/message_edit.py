import jwt
import threading
from .database import *
from .access_error import *

def message_edit(token, message_id, message):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]
    
    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, True):
        raise AccessError(description="This token is invalid")

    # Message is more than 1000 characters
    if len(message) > 1000:
        raise ValueError(description="Messages must be less than 1000 characters")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    channel_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id:
                channel_ = channel
                break
    
    if channel_ is None:
        raise ValueError(description="Channel does not exist")

    obj_request = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            obj_request = user
            break

    user_id = obj_request.get_u_id()
    # the message is not existed
    if user_id is None:
        raise AccessError(description="The message is not existed")

    # if user is not the poster and admin
    if u_id != user_id:
        raise AccessError(description="You don't have access to delete")
    
    # update the database with new message
    channel._messages.test = message
            
