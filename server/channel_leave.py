from channel_list import channel_list
from channel_details import channel_details


def channel_leave(token, channel_id):
    # somehow get the associated uid
    uid_ = 111

    # check if channel exists, if it does not throw a ValueError
    if channel_id not in channel_list(token):
        raise ValueError

    # otherwise remove the user with this token from the channel
    for index, user in enumerate(channel_details(channel_id)['all_members']):
        if user["uid"] == uid_:
            del channel_details(channel_id)['all_members'][index]
            break
