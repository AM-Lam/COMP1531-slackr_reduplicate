from .channel_join import channel_join
from .database import *


def channel_invite(token, channel_id, u_id):
    # here check if token is a valid token.
    if token in update_data['tokens'].keys():
        verify_user_validity(u_id)
        verify_token_not_member(token, channel_id, u_id)
        # now that all the detals have been verified we join the user to the channel
        channel_join(token, channel_id) ##<--------------------------------------
        return {}
    else:
        raise ValueError("the given token does not exist")
      

def verify_token_not_member(token, channel_id, u_id):
    SECRET = get_secret()
    decode = (jwt.decode(token, SECRET, algorithm = 'HS256'))
    user_id = decode['u_id']
    flag = 0
    for i in update_data['channels']:
        for j in i.member
            if user_id == j:
                flag = 1
    if flag == 1:
        raise ValueError("user already exists in the channel") 

def verify_user_validity(u_id):
    flag = 0
    for users in update_data['users']:
        if users._u_id == u_id:
            flag = 1
    if flag == 0:
        raise ValueError("user id does not exist on the server")
