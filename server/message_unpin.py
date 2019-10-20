from .channels_list import channels_list

def message_unpin(token, message_id):
    #  message_id is not a valid message
    if message_id not in message_id_list:
        raise ValueError("Message is not exists.")

    #  The authorised user is not an admin
    if id_of_channel not in channels_list(token_of_message):
        raise ValueError("Sorry, you don't have access to unpin the message.")
    
    #  Message with ID message_id is already unpinned
    if token not in pinned_list[message_id]:
        raise ValueError("The message is not pinned. Please try again.")

    #  The authorised user is not a member of the channel that the message is within
    # check whether the user is a member in the channel or not
    token_of_message = message_id_dic[message_id][0]
    id_of_channel = message_id_dic[message_id][1]
    if id_of_channel not in channels_list(token_of_message):
        raise AccessError("You are not a member in the channel.")
    
    # if the function is working
    pinned_list[message_id].remove(token)
