from .access_error import AccessError
from .channels_list import channels_list

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
    # if channel_slist succeed, it should list of channels that the user being
    # check whether the user is a member in the channel or not
    if id_of_channel not in channels_list(token_of_message):
        if permission_id_dic[token_of_message][id_of_channel] == 3:  
            #  Person who make the request is not an admin or owner in the channel so they don't have permission to remove the message
            raise AccessError("You don't have access to remove the message. Only the sender or admin shall make this request.")
    else: 
        # Since it also fail the channel_details so something must be wrong with the token or channel
        raise AccessError("You are not a member in this channel")
    
    #If the function is successfully executed
    del message_id_dic[message_id]
    message_id_list.remove(message_id)
