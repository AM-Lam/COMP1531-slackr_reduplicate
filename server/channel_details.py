from .access_error import AccessError


def channel_details(token, channel_id):
    check_channel_existence(channel_id)
    verify_user_status(token)
    # return name, ownermembers all members----> {"name" = name, "owner_members" = owner_members, "all_members" = all_members}
    pass

def check_channel_existence(channel_id):
    # this function will have to check and verify if the channel is valid
    pass

def verify_user_status(token, channel_id):
    # this will check if the user is a part of the channel
    pass