import setup
from setup import channel_id_dic
from setup import message_id_list
from setup import message_id_dic
from setup import permission_id_list
from setup import permission_id_dic
from setup import AccessError
from channels_list import channels_list

def message_edit(token, message_id, message):
    # basic case
    # if the message_id cannot be found
    if message_id not in message_id_list:
        raise ValueError("The message is not existing. Please try again.")

    #  Message with message_id edited by authorised user is not the poster of the message
    token_of_message = message_id_dic[message_id][0]
    id_of_channel = message_id_dic[message_id][1]

    if token_of_message != token:
        raise ValueError("You don't have access to edit the message as you are not the poster of the message.")

    #  Message with message_id is not a valid message
    if permission_id_dic[token_of_message][id_of_channel] == 3:
    #     1) is a message sent by the authorised user
    # message doesn't have the right format or character limitation. E
    # Even though it is sent by the right person the request is still denied
        if (len(message) > 1000):
            raise ValueError("The message is too long. Please keep it within 1000 characters.")   
    #     2) If the authorised user is an admin, is a any message within a channel that the authorised user has joined
    else:
        raise ValueError("Admin don't have the permission to edit the message. ")   

    #psedo-code
    # if the function is executed, i suppose this is the way to change the message's content
    message_id_list[message_id] = message
