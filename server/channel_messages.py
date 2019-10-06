from access_error import AccessError 


def channel_messages(token, channel_id, start):
    does_channel_exist(channel_id)
    is_start_greater_then_messages(start)
    is_token_a_member_of_channel(token, channel_id)
    # code here towards the return values.
    return {'messages' : messages , 'start' : start , 'end' : end}
    pass

def does_channel_exist(channel_id):
    # this function will check is the channel id refers to a valid channel!
    pass

def is_start_greater_then_messages(start):
    # this will check if given start(num) is > then the total no. of messages!
    pass

def is_token_a_member_of_channel(token, channel_id):
    # this will raise an access error if user(token) is not a member of this channel!
    pass