from .access_error import AccessError
from .channels_list import channels_list


def channel_addowner(token, channel_id, u_id):
    # first get the u_id from the user token
    owner_uid = 111
    
    to_add = None
    # now check whether or not the channel actually exists, if it does exist
    # set it to a value and break out of the loop earlier
    for channel in channels_list(owner_uid)["channels"]:
        if channel["channel_id"] == channel_id:
            to_add = channel
            break
    
    # if the channel requested does not exist or the u_id is already an owner of
    # it raise an error, this will probably need to interact with a database
    # if to_add == None or channel_owner(u_id, to_add["channel_id"]):
    #    raise ValueError
    
    # now make sure the calling user has the permissions to make this change, we
    # will need a few functions to be written that access a database for this to
    # work
    # if not slackr_owner(owner_uid) and not channel_owner(owner_uid, channel_id):
    #    raise AccessError("Lack permissions to add owner to this channel")
    
    # finally set the u_id to be an owner of the channel requested, we will need
    # to interact with a database to handle this
    
    return {}
    
