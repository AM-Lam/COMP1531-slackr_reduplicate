import setup
from channel_list.file import channel_list

token = setup.generateToken('hayden@gmail.com', '123456', 'Hayden', 'Smith')
channel_id_list = {'channel 1', 'Channel 1', 'channel1'}
message_id = "456789"
# format of message_id_dic: 'message_id':{'token', 'channel_id'}
message_id_dic = {'message_id': {'123', 'channel1'}, 'message': {'456', 'channel 1'}, 'id': {'123', 'Channel 1'}}
message_id = setup.generateMessage(token, channel_id, message)
permission_id = {'123': 'member' ,'456': 'admin', '789': 'member', 'AD': 'admin', '159': owner}
#format of pinned_list = {token: message_id}
pinned_dic = {'message_id':'123', 'id': '123'}

def message_pin(token, message_id):
    # ValueError when:
    #  message_id is not a valid message
    if message_id not in message_id_dic:
        raise ValueError("Message is not exists.")
    #  The authorised user is not an admin
    if message_id_dic[message_id][0] == 'member':
        raise ValueError("Sorry, you don't have access to pin the message.")
    #  Message with ID message_id is already pinned
    if message_id in pinned_dic:
        raise ValueError("The message is pinned.")
    # AccessError when:
    #  The authorised user is not a member of the channel that the message is within
    # check whether the user is a member in the channel or not
    token_of_message = message_id_dic[message_id][0]
    if message_id_dic[message_id][1] in channel_list(token_of_message):
        raise AccessError("You are not a member in the channel.")
    
    
def message_unpin(token, message_id):
    pass
