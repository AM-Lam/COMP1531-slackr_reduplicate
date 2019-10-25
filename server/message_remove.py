#from .database import *
import jwt
# from .access_error import AccessError
import access_error
#from .channels_list import channels_list
import channels_list

def is_admin(u_id, obj_channel):
    if u_id in obj_channel._members:
        for person in obj_channel._members:
            # and the request is sent by member of the channels
            if person[u_id] == 'admin':
                return True
    return False

def message_remove(token, message_id):

    server_data = get_data()
    # Message (based on ID) no longer exists
    # or the message Id never exists
    if message_id not in server_data['channels']._messages:
        raise ValueError #("The message is not existing. Please try again")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # not an authorised user
    if token not in server_data['token']:
        raise access_error.AccessError 

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    for channel in server_data['channels']:
        for message in channel._messages:
            # the message is not existed
            # double check
            if message_id not in message._message_id:
                raise access_error.AccessError 

            if message._message_id == message_id:
                # if the request is not send by the poster 
                if message._u_id != u_id:
                        if is_admin(u_id, channel) == False:
                            raise access_error.AccessError 
                channel._messages.remove(message)
            

            

#200, 400,404,500