from .access_error import *
from .database import *
import jwt


def channel_messages(token, channel_id, start):
    end = 0
    does_channel_exist(channel_id)                             # checking if the channel exist.
    end = is_start_greater_then_messages(start, channel_id)    # checks if (start + 50) is greater then the total messages.         
    is_token_a_member_of_channel(token, channel_id)            # this will check if the user is a member of the channel.
    messages = retrive_message_list(channel_id, start, end)         # this function retrives a message list.
    return {'messages' : messages , 'start' : start , 'end' : end}
    

def does_channel_exist(channel_id):
    update_data = get_data()
    flag = 0
    for channels in update_data['channels']:    # looping through the channels list.
        if channels._channel_id == channel_id:  # set flag as one if channel exists.
            flag = 1
    if flag == 0:
        raise ValueError(description="channel given does not exist!")


def is_start_greater_then_messages(start, channel_id):
    update_data = get_data()
    length = 0                  # initializing the total messages to zero.
    start_to_end = start + 50   # adding 50 to the given start to get the expected end.
    overflow_value = -1         # this is returned if expected end is greater then the number of messages.
    for channel in update_data['channels']:
        if channel._channel_id == channel_id:
            length = len(channel._messages)    # now length is the total number of messages in the channel.
    if start_to_end > length:
        return overflow_value   # return -1 is expected end is greater then the number of messages.
    else:
        return start_to_end     # return expected end num if expected end is <= number of messages in the channel.

def is_token_a_member_of_channel(token, channel_id):
    # this will check if the user is a part of the channel.
    update_data = get_data()
    SECRET = get_secret()
    decode = (jwt.decode(token, SECRET, algorithm = 'HS256'))    # extracting u_id from token.
    user_id = decode['u_id']    
    flag = 0
    for channel in update_data['channels']:
        if channel._channel_id == channel_id:
            for people in channel._members:                
                if people == user_id:
                    flag = 1                    # flag is one if the user is a member of the channel.    
    if flag == 0:
        raise AccessError(description='user is not a part of the channel... does not have correct permissions.')

def retrive_message_list(channel_id, start, end):
    update_data = get_data()
    messages = []                               # initialising a messages list.
    for channel in update_data['channels']:     # looping through the channels list(high-level). 
        if channel._channel_id == channel_id:   # if we find the correct channel then go into the channel.
            length = len(channel._messages)     # retriving the number of messages in that channel.
            if start <= length:
                if end == -1:                       # if end is -1 then we want to return all remaining messages.
                    idx = 1 + start                 # idx is the index for the message list. starts at 1 because if start is zero then we want the index for the first message to be 1.
                    # looping through the message list reversed, because we want the most recent message first 
                    # and using splicing to specify message range.
                    rev_list = channel._messages[::-1]
                    for i in rev_list[start:length]:  
                        diction = {'message_id':idx , 'u_id':i._u_id , 'message':i._text , 'time_created':i._time_sent , 'reacts':i._reacts , 'is_pinned':i._pinned}
                        messages.append(diction)
                        idx += 1
                else:
                    idx = 1 + start
                    # looping through the message list reversed, because we want the most recent message first 
                    # and using splicing to specify message range.
                    rev_list = channel._messages[::-1]
                    for i in rev_list[start:end]:
                        diction = {'message_id':idx , 'u_id':i._u_id , 'message':i._text , 'time_created':i._time_sent , 'reacts':i._reacts , 'is_pinned':i._pinned}
                        messages.append(diction)
                        idx += 1
            else:
                raise ValueError('start is greater then the total number of messages!')
    return messages