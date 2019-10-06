from auth_register.file import auth_register
from channel_create.file import channel_create

class AccessError(Exception): 
    pass

class Error(Exception):
    pass

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
    message_id_dic = message_send(token,channel_id, message)
    message_id = channel_create_dic[message]
    return message_id
# hardcore the user 
#format of u_id_list: {token: u_id}
u_id_list = {'person1':123, 'person2':456,'person3':789, 'admin1': 11, 'admin2': 22, 'owner': 159}
#u_id_dic:{u_id: {token, email, first name, last name, handle}}
u_id_dic = {
    123: {'hayden@gmail.com', 'Hayden', 'Smith', 'Hayden'},
    456:{'smith@gmail.com', 'Smith', 'Hayden', 'Smith'},
    789:{'person@gmail.com', 'one', 'person', '1st'},
    11:{'admin1@gmail.com', 'one', 'admin', 'admin1'},
    22:{'admin2@gmail.com', 'two', 'admin', 'admin2'},
    159:{'owner@gmail.com', 'Owner', 'UNSW', 'handler'}
}

# channel_id_dic: {channel_id: channel name}
channel_id_dic = {1: 'channel 1', 2: 'Channel 1', 3: 'channel1'}

# record of existing message
# message_id_list = {message_id: "message"}
message_id_list = {1: "hi", 2:"hello", 3:"yo", 4: "sdfsa", 5: "65456"}

# message_id_dic: 'message_id':{'token', 'channel_id'}
message_id_dic = {
    1: {'person1', 1}, 
    2: {'person1', 2}, 
    3: {'person2', 3},
    4: {'person2', 3},
    5: {'admin1', 1}
}

permission_id_list: {1, 2, 3}

# Based on different channels user have different permission
# permission_id_dic = {token: {channel_id: permission_id}}
permission_id_dic = {
    'person1': {1: 3, 2: 3},
    'person2': {2: 3},
    'person3': {1: 3, 2: 3, 3: 3},
    'admin1': {1: 2, 2: 3},
    'admin2': {2: 2, 3: 3},
    'owner': {1: 1, 2: 1, 3: 1}
}

# format of react_id_dic: message_id: {token, messsage_id, react_id}
react_id_dic = {
    1: {'owner', 1, 1}, 
    2: {'person3', 2, 5}
}

react_id_type = {1:'like', 2:'love', 3:'sad', 4:'hate', 5:'smile', 6:'angry'}

#pinned_list: {message_id: token}
pinned_list = {1: 'admin1', 5: 'owner'}


# token = generateToken('hayden@gmail.com', '123456', 'Hayden', 'Smith')
# channel_id = generateChannel(token, "Channel 1", True)
# message_id = generateMessage(token, channel_id, "message")
