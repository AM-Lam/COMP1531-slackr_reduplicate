import jwt
import threading
from .database import *
from .access_error import *

def message_unpin(token, message_id):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
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

    user_ = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            user_ = user
            break
    
    if user_ == None:
        raise ValueError("u_id does not belong to a real user")

    if message_ is None:
        raise ValueError(description="The provided id does not refer to a real message")
    
    if user_.is_global_admin() == False and u_id not in channel_.get_owners():
        raise ValueError(description="Only admins and owners can unpin messages!")
    #  Message with ID message_id is already pinned
    if message_._pinned == False:
        raise ValueError(description="The message is not pinned")
    else:
        # pin the message and add it to the channels list of pins
        message_._pinned = False
        channel_._pinned_messages.remove(message_.get_m_id())
    
    return {}