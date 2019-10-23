from .database import *
import jwt


def message_send():
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

