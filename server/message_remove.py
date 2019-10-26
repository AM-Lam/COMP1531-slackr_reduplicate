import jwt
import threading
from .database import *
from .access_error import *

def message_remove(token, message_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # not an authorised user
    if token not in server_data["token"]:
        raise AccessError(description="This token is invalid")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    channel_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        if channel.get_id() == channel_id:
            channel_ = channel
            break
    
    if channel_ is None:
        raise ValueError(description="Channel does not exist")
    
    # Message (based on ID) no longer exists
    # or the message Id never exists
    user_mid_ = None
    for message in server_data['channels']._messages:
        if message_id == message._m_id():
            user_id_ = message.get_u_id

    # the message is not existed
    if user_mid == None:
        raise AccessError(description="The message is not existed")
 
    if u_id != user_mid:
        # if user is not the poster and admin
        if not u_id.is_global_admin():
            raise AccessError(description="You don't have access to delete")
    
    # add the message to the server database
    channel._messages.remove(message)
            

            

#200, 400,404,500