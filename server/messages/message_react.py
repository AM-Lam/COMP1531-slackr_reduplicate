from setup import channel_id_dic
from setup import message_id_list
from setup import message_id_dic
from setup import react_id_dic
from channels_list import channels_list

def message_react(token, message_id, react_id):
    # assume we can get the list of channels that the user's joining by getting u_id's dictionary
    # message_id is not a valid message within a channel that the authorised user has joined
    # message does not exist
    if message_id not in message_id_list:
        raise ValueError("The message no longer exists.")

    # user is not in the channel anymore
    token_of_message = message_id_dic[message_id][0]
    id_of_channel = message_id_dic[message_id][1]
    if id_of_channel not in channels_list(token_of_message):
        raise ValueError("You are not a member of the channel.")

    #  react_id is not a valid React ID
    if react_id not in react_id_type:
        return ValueError("Please enter a valid react_id.")
    #  Message with ID message_id already contains an active React with ID react_id
    if react_id_dic[message_id][2] != None:
        return ValueError("You reacted before. Please don't repeat.")

    # if the function is working
    # add the react_id into dictionary
    react_id_dic[message_id] = {token, message_id, react_id}
    
