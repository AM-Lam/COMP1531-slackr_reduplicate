from .channels_list import channels_list

    
def message_unreact(token, message_id, react_id):
 
    #  message_id is not a valid message within a channel that the authorised user has joined
    if message_id not in message_id_list:
        message_unreact(token, message_id)
        raise ValueError("The message no longer exists.")

    # user is not in the channel anymore
    token_of_message = message_id_dic[message_id][0]
    id_of_channel = message_id_dic[message_id][1]
    if id_of_channel not in channels_list(token_of_message):
        raise ValueError("Invalid message.")

    #  react_id is not a valid React ID
    if react_id not in react_id_type:
        return ValueError("Please enter a valid react number.")

    #  Message with ID message_id already contains an active React with ID react_id
    if react_id_dic[message_id][2] == None:
        return ValueError("You haven't raect on this message.")

    # If the function is working, delete the record of react in dictionary    
    del react_id_dic[react_id]
