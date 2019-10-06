from access_error import AccessError
from channels_listall import channels_listall


def channel_join(token, channel_id):
    # first try to get the relevant u_id from the provided token, this will need
    # us to interact with a database and retrieve data presumably
    u_id = 111
    
    # next we have to check whether or not the given user is an admin, again
    # we'll probably need to interact with a db for this
    # is_admin = user_is_admin(u_id)
    found_channel = False

    for channel in channels_listall(token)["channels"]:
        # somehow check if the channel is private, another database interaction
        # it should probably look like what's below
        # if channel_private(channel["channel_id"]) and not is_admin:
        #   raise AccessError("Cannot join private channel as regular user")
        
        if channel["channel_id"] == channel_id:
            found_channel = True
            break

    if not found_channel:
        raise ValueError

    # add the user's u_id to the channel's list of members, since the data we 
    # get using channels_listall appears to be read-only
    
    return {}    
    
