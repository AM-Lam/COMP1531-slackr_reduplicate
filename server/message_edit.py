from .database import *
import jwt
from .access_error import AccessError
from .channels_list import channels_list

def message_edit(token, message_id, message):
    server_data = get_data()

    # basic case
    # if the message_id cannot be found
    if message_id not in server_data['channels']._messages:
        raise ValueError 
        
        # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    for channel in server_data['channels']
        for message in channel._messages
            # the message is not existed
            # double check
            if message_id not in message._message_id:
                raise AccessError 

            if message._message_id == message_id:
                # if the request is not send by the poster 
                # only poster is able to edit
                if message._u_id != u_id:
                    raise AccessError 
                    #     1) is a message sent by the authorised user
                    # message doesn't have the right format or character limitation. 
                    # Even though it is sent by the right person the request is still denied
                if len(message) > 1000:
                    raise ValueError
                # update the database with new message
                # or use update data?
                channel._messages.test = message
