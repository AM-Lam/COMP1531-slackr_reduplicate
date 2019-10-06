import setup
from channel_list.file import channel_list

token = setup.generateToken('hayden@gmail.com', '123456', 'Hayden', 'Smith')
channel_id_dic = {1:channel 1, 2:'Channel 1', 3:'channel1'}
message_id = "456789"
# format of message_id_dic: 'message_id':{'token', 'channel_id'}
message_id_dic = {'message_id': {'123', 'channel1'}, 'message': {'456', 'channel 1'}, 'id': {'123', 'Channel 1'}}
message_id = setup.generateMessage(token, channel_id, message)
#Based on different channels user have different permission

#permission_id_dic = {'123': 'member' ,'456': 'admin', '789': 'member', 'AD': 'admin', '159': owner}

#format of pinned_dic = {token: message_id}
pinned_list = {'message_id', 'id'}

def message_pin(token, message_id):

    #  message_id is not a valid message
    if message_id not in message_id_dic:
        raise ValueError("Message is not exists.")
    #  The authorised user is not an admin
    if message_id_dic[message_id][0] == 'member':
        raise ValueError("Sorry, you don't have access to pin the message.")
    #  Message with ID message_id is already pinned
    if message_id in pinned_list:
        raise ValueError("The message is pinned.")

    #  The authorised user is not a member of the channel that the message is within
    # check whether the user is a member in the channel or not
    token_of_message = message_id_dic[message_id][0]
    if message_id_dic[message_id][1] in channel_list(token_of_message):
        raise AccessError("You are not a member in the channel.")
    
    # if the function is working
    pinned_list.append = message_id
    
def message_unpin(token, message_id):
    #  message_id is not a valid message
    if message_id not in message_id_dic:
        raise ValueError("Message is not exists.")
    #  The authorised user is not an admin
    if message_id_dic[message_id][0] == 'member':
        raise ValueError("Sorry, you don't have access to unpin the message.")
    #  Message with ID message_id is already unpinned
    if message_id not in pinned_list:
        raise ValueError("The message is unpinned.")

    #  The authorised user is not a member of the channel that the message is within
    # check whether the user is a member in the channel or not
    token_of_message = message_id_dic[message_id][0]
    if message_id_dic[message_id][1] in channel_list(token_of_message):
        raise AccessError("You are not a member in the channel.")
    
    # if the function is working
    pinned_list.remove(message_id)