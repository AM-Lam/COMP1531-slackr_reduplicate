from .channel_join import  channel_join


def channel_invite(token, channel_id, u_id):
    verify_user_validity(u_id)
    verify_token_not_member(token, channel_id, u_id)
    # now that all the detals have been verified we join the user to the channel
    channel_join(token, channel_id) ##<--------------------------------------
    pass  

def verify_token_not_member(token, channel_id, u_id):
    # this function will check if the member being invited currently does not exist in the channel
    pass

def verify_user_validity(u_id):
    # this function checks if the user even exists on the applications database
    pass
