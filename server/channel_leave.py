# comment this out until these functions are written
from .channels_list import channels_list
from .channel_details import channel_details


def channel_leave(token, channel_id):
    # somehow get the associated uid, this will presumably need
    # to interact with a database or something similar
    uid_ = 111

    # check if channel exists, if it does not throw a ValueError
    if channel_id not in [c["channel_id"] for c in channels_list(token)]:
        raise ValueError

    # otherwise remove the user with this token from the channel
    for user in channel_details(channel_id)['all_members']:
        if user["u_id"] == uid_:
            # at this point we will need to interact with a database
            # to remove this u_id from the list of members
            return {}

