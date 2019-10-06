import setup
from setup import channel_id_dic
from setup import message_id_list
from setup import message_id_dic
from setup import permission_id_list
from setup import permission_id_dic
from setup import AccessError
from channel_list.file import channel_list

# TODO
# Have to include the related file name later
from channel_list.file import channel_list

def message_send(token, channel_id, message):
    # Message is more than 1000 characters
    if (len(message) > 1000):
        raise ValueError("The message is too long. Please keep it within 1000 characters.")   
    
    # if the user id not a member of the channel
    if permission_id_dic[token][channel_id] == None:
        raise AccessError("You don't have access in this channel. Please try again after you join.")

    message_id_dic = sorted(message_id_dic.items())
    leng = message_id_dic.keys()[-1]
    message_id_dic[leng + 1]
    message_id_list[message_id] = message

def message_remove(token, message_id):
    # Message (based on ID) no longer exists
    # or the message Id never exists
    if message_id not in message_id_list:
        raise ValueError("The message is not existing. Please try again")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    if message_id_dic[message_id][0] != token:
        raise AccessError("You have no permission to remove the message. Messages can only be deleted by sender or admin.")

    token_of_message = message_id_dic[message_id][0]
    id_of_channel = message_id_dic[message_id][1]
    # if channel_list succeed, it should list of channels that the user being
    # check whether the user is a member in the channel or not
    if id_of_channel not in channel_list(token_of_message):
        if permission_id_dic[token_of_message][id_of_channel] == 3:  
            #  Person who make the request is not an admin or owner in the channel so they don't have permission to remove the message
            raise AccessError("You don't have access to remove the message. Only the sender or admin shall make this request.")
    else: 
        # Since it also fail the channel_details so something must be wrong with the token or channel
        raise AccessError("You are not a member in this channel")
    
    #If the function is successfully executed
    del message_id_dic[message_id]
    message_id_list.remove(message_id)

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
