import jwt
from .database import get_data, get_secret
from .access_error import *

def message_remove(token, message_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    message_ = None
    
    # check if this channel
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id:
                message_ = message
                break
    
    if message_ is None:
        raise ValueError(description="Message does not exist")

    user_ = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            if user.get_u_id() != message_.get_u_id() and not user.is_global_admin():
                break
            user_ = user
            break

    if user_ == None:
        # if user is not the poster or an admin
        raise AccessError(description="You don't have access to delete")
    
    # remove the message to the server database
    channel._messages.remove(message)

    return {}
