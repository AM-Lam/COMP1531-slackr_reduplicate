def channels_create(token, name, is_public):
    # first check for a valid name
    if len(name) > 20:
        raise ValueError
    
    # now grab the u_id associated with the provided token
    u_id = 111
    
    # at this point we'll have to interact with a database, and add a new
    # channel to it, this will likely include incrementing a value to get the
    # channel_id, but we clearly can't do this at this stage of development
    channel_id = 101
    
    # return the new channel's id
    return { "channel_id" : channel_id }
