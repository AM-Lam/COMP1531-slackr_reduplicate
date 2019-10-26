from .database import *
from .access_error import AccessError


def channel_details(token, channel_id):
    update_data = get_data()
    if token in update_data['tokens'].keys():  # here check if token is a valid token.
        check_channel_existence(channel_id)    # this will check if the chanel exists. 
        details = verify_user_status(token)    # this will check if the user is in the channel and will get channel details.
        return details
    else:
        raise ValueError("the given token does not exist")

def check_channel_existence(channel_id):
    # this function will have to check and verify if the channel is valid
    update_data = get_data()
    flag = 0
    for channels in update_data['channels']:    # looping through the channels list.
        if channels._channel_id == channel_id:  # set flag as one if channel exists.
            flag = 1
    if flag == 0:
        raise ValueError("channel given does not exist!")

def verify_user_status(token, channel_id):
    # this will check if the user is a part of the channel
    update_data = get_data()
    SECRET = get_secret()
    decode = (jwt.decode(token, SECRET, algorithm = 'HS256'))    # extracting u_id from token.
    user_id = decode['u_id']    
    flag = 0
    for channel in update_data['channels']:
        if channel._channel_id == channel_id:
            for people in channel._members:                
                if people == user_id
                    flag = 1                    # flag is one if the user is a member of the channel.    
    if flag == 1:
        c_name = channels._channel_name
        c_omembers = channels._owners
        c_amembers = channels._members
        return {"name" : c_name, "owner_members" : c_omembers, "all_members" : c_amembers} 
    else:
        raise AccessError('user is not a part of the channel... does not have correct permissions.')
