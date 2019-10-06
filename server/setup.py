 # for the import, I don't know the file name
# TODO
from auth_register.file import auth_register
from channel_create.file import channel_create
from message_(un)sendOredit import message_send

# token = generateToken('hayden@gmail.com', '123456', 'Hayden', 'Smith')
# channel_id = generateChannel(token, "Channel 1", True)
# message_id = generateMessage(token, channel_id, message)

#format of u_id_dic: {u_id: token}
# u_id_dic = {'123': '123', 456': '456', '789': '789', '159': '159', 'AD': 'AD'}

# token = setup.generate_token('hayden@gmail.com', '123456', 'Hayden', 'Smith')
# channel_id = setup.generate_channel(token, "Channel 1", True)
# channel_id_list = {'channel 1', 'Channel 1', 'channel1'}
# message_id = "456789"
# # format of message_id_dic: 'message_id':{'token', 'channel_id'}
# message_id_dic = {'message_id': {'123', {'channel1', 'Channel 1'}}, 'message': {'456', {'channel 1', 'Channel 1', 'channel1'}}, 'id': {'123', 'Channel 1'}}
# permission_id = {'123': 'member' ,'456': 'admin', '789': 'member', 'AD': 'admin', '159': owner}

class AccessError(Exception): 
    pass

class Error(Exception):
    pass
    
def auth_register(email, password, firstN, lastN):
    return {"123456": 1, "token": 123456}

def channel_create(token, name, is_public):
    return {"123456": 3, "channel_id": 123456}

# Hayden's video on Testing Help https://youtu.be/1WePByrzU5I
def generate_token(email, password, firstN, lastN):
    auth_register_dic = {}
    auth_register_dic = auth_register(email, password, firstN, lastN)
    token = auth_register_dic[firstN]
    return token
    
def generate_channel(token, name, is_public):
    channel_create_dic = {}
    channel_create_dic = channel_create(token, name, is_public)
    channel_id = channel_create_dic[name]
    return channel_id

def generate_message(token, channel_id, message):
    message_id_id_dic = {}
    message_id_dic = message_send(token,channel_id message)
    message_id = channel_create_dic[message]
    return message_id
