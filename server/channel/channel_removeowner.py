from channels_list import channels_list


def channel_removeowner(token, channel_id, u_id):
    # first get the u_id from the user token
    owner_uid = 111
    
    to_add = None
    # now check whether or not the channel actually exists, if it does exist
    # set it to a value and break out of the loop earlier
    for channel in channels_list(token)["channels"]:
        if channel["channels_id"] == channel_id:
            to_add = channel
            break
    
    # if the channel requested does not exist or the u_id is not an owner of it
    # raise an error
    if to_add == None:
        raise ValueError

    # checking whether the user is not an owner will require acces to a db
    
    # now make sure the calling user has the permissions to make this change, we
    # will need a few functions to be written that access a database for this to
    # work
    # if not slackr_owner(owner_uid) and not channel_owner(owner_uid, channel_id):
    #    raise AccessError("Lack permissions to add owner to this channel")
    
    # finally remove the u_id as an owner of the channel requested, we will need
    # to interact with a database to handle this
    return {}

