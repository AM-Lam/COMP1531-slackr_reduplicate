import jwt
import threading
from .database import *
from .access_error import *

def message_unpin(token, message_id):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, True):
        raise AccessError(description="This token is invalid")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # Message (based on ID) no longer exists
    # or the message Id never exists
    if message_id not in server_data['channels']._messages:
        raise ValueError #("The message is not existing. Please try again")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    for channel in server_data['channels']:
        for message in channel._messages:
            # the message is not existed
            # or the channel is not existed
            if message_id not in message._message_id:
                raise AccessError 

            if message._message_id == message_id:
                # if the request is not send by the poster 
                if message._u_id != u_id:
                    #  The authorised user is not an admin
                    if is_admin(u_id, channel) == False:
                        raise AccessError 

            #  Message with ID message_id is not pinned
            if message._pinned == False:
                raise ValueError
            else: 
                message._pinned == False
    