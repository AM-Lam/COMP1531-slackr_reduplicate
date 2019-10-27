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
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # Message is more than 1000 characters
    if len(message) > 1000:
        raise ValueError(description="Messages must be less than 1000 characters")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    message_ = None
    channel_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for m in channel._messages:
            if m.get_m_id() == message_id:
                channel_ = channel
                message_ = m
                break
    
    if message_ is None:
        raise ValueError(description="Message does not exist")

    user_ = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            if message_.get_u_id() != u_id and not user.is_global_admin() and not u_id in channel_.get_owners():
                break
            user_ = user
            break

    # if user is not the poster or admin
    if user_ is None:
        raise AccessError(description="You do not have permission to edit this message")
    
    print(f'Message object {message_} has text {message_.get_text()}')
    # update the database with new message
    message_.edit_text(message)
    print(f'Message object {message_} has text {message_.get_text()}')
            
    return {}
