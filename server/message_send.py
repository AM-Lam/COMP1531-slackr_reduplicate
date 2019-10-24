from .database import *
import jwt


def message_send(token, channel_id, message):
    # Message is more than 1000 characters
    if len(message) > 1000:
        raise ValueError# ("The message is too long. Please keep it within 1000 characters.")   
    
    # if the user id not a member of the channel
    # TODO
    # verify token
    if permission_id_dic[token][channel_id] == None:
        raise AccessError #("You don't have access in this channel. Please try again after you join.")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]
    
    server_data = get_data()

    # make our message id just be the count of messages we already have
    # incremented by 1, this way the message_ids will increase sequentially
    message_id = len(server_data["message"]) + 1

    # TODO
    time_sent=
    # at the start there will be no messages and the only member will be
    # the creator of the channel
    new_message = Messages(message, [u_id], message, channel_id, time_sent)
    
    # add the message to the server database
    server_data["message"].append(new_message)

    # return the new message's id
    return { "message_id" : message_id }

