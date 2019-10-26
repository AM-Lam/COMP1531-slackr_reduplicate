import jwt
import threading
from .database import *
from .access_error import *

def message_pin(token, message_id):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, True):
        raise AccessError(description="This token is invalid")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    channel_ = None
    message_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id:
                channel_ = channel
                message_ = message
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

    if u_id != user_id:
        # if user is not the poster and admin
        if not obj_request.is_global_admin():
            raise AccessError(description="You don't have access to delete")

    #  Message with ID message_id is already pinned
    if message_._pinned == True:
        raise ValueError(description="The message is pinned")
    else: 
        message_._pinned == True
