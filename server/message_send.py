import jwt
from .database import *
from datetime import datetime 
from .access_error import AccessError
from .channels_list import channels_list

def message_send(token, channel_id, message):
    # Message is more than 1000 characters
    if len(message) > 1000:
        raise ValueError
    
    server_data = get_data()

    # not an authorised user
    if token not in server_data['token']:
        raise AccessError 

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # not an authorised user
    if token not in server_data['token']:
        raise AccessError 

    # if the user id not a member of the channel
    if u_id not in channels_list(list):
        raise AccessError 
    
    # make our message id just be the count of messages we already have
    # incremented by 1, this way the message_ids will increase sequentially
    message_id = len(server_data["message"]) + 1
    time_sent = str(datetime.now())

    # at the start there will be no messages and the only member will be
    # the creator of the channel
    new_message = Messages(message_id, u_id, message, channel_id, time_sent, [])
    
    channels_list = channels_list(token)
    # add the message to the server database
    for channel in channels_list:
        if channel.channel_id == channel_id:
            channel.messages.append(new_message)

    # return the new message's id
    return { "message_id" : message_id }

