from .database import *
import jwt
from .channels_list import channels_list

def message_pin(token, message_id):
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
        raise AccessError 

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    for channel in server_data['channels']
        for message in channel._messages
            # the message is not existed
            # or the channel is not existed
            if message_id not in message._message_id:
                raise AccessError 

            if message._message_id == message_id:
                # if the request is not send by the poster 
                if message._u_id != u_id:
                        if u_id in channel._members:
                            for person in channel._members:
                                # and the request is sent by member of the channels
                                if person[u_id] == 'member':
                                    raise AccessError 
                        # the user who send the request is not a member of the channel
                        else: 
                            raise AccessError 

            if 


    #  Message with ID message_id is already pinned
    if token in pinned_list[message_id]:
        raise ValueError("The message is pinned.")

    #  The authorised user is not a member of the channel that the message is within
    # check whether the user is a member in the channel or not
    token_of_message = message_id_dic[message_id][0]
    id_of_channel = message_id_dic[message_id][1]
    if id_of_channel not in channels_list(token_of_message):
        raise AccessError("You are not a member in the channel.")
    
    # if the function is working
    pinned_list[message_id].append(token)
    
