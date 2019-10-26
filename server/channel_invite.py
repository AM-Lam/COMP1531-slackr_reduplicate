from .access_error import AccessError
from .channel_join import channel_join
from .database import *
import jwt
import time


def channel_invite(token, channel_id, u_id):
    update_data = get_data()
    if token in update_data['tokens'].keys():  # here check if token is a valid token.
        SECRET = get_secret()                  # getting the secret from the database. 
        verify_channel_exists(channel_id)      # making sure that the channel exists.
        verify_user_validity(u_id)             # verifing that the user actually exists in the database.
        verify_token_not_member(token, channel_id, u_id)    # verifiy that the uid is not a part of the channel.   
        encoded = jwt.encode({'u_id': u_id , 'time': time.time()}, SECRET, algorithm='HS256').decode()
        # we are not adding this new token to the active tokes list bc this is not a login function.
        channel_join(encoded, channel_id)      # now that all the detals have been verified we join the user to the channel.
        return {}
    else:
        raise ValueError("the given token does not exist")
      

def verify_token_not_member(token, channel_id, u_id):
    update_data = get_data()
    SECRET = get_secret()               # getting the secret from thd database.
    decode = (jwt.decode(token, SECRET, algorithm = 'HS256'))    # extracting u_id from token.
    user_id = decode['u_id']            
    # checking if token is in the channel
    flag_2 = 0
    for k in update_data['channels']:    # going through the channels list.
        for userss in k._members:        # going through the members of the channel list.
            if user_id == userss:  # setting flag to 1 if user id was found in the channel.
                flag_2 = 1
    if flag_2 == 0:
        raise AccessError("user trying to add another member is not a part of the channel")
    # making sure the u_id trying to be added is not in the channel
    flag = 0                                
    for i in update_data['channels']:   # going through the channels list.
        for users in i._members:        # going through the members of the channel list.
            if u_id == users:     # setting flag to 1 if user id was found in the channel.
                flag = 1
    if flag == 1:
        raise ValueError("user already exists in the channel") 

def verify_user_validity(u_id):
    update_data = get_data()
    flag = 0                              # If flag is zero then the user deos not exist!
    for users in update_data['users']:    # looking through the users list.
        if users._u_id == u_id:
            flag = 1
    if flag == 0:
        raise ValueError("user id does not exist on the server")

def verify_channel_exists(channel_id):
    update_data = get_data()
    flag = 0
    for i in update_data['channels']:
        if channel_id == i._channel_id:
            flag = 1
    if flag == 0:
        raise ValueError('channel does not exist')
