import jwt
from .access_error import *
from .database import *
from .channels_list import channels_list


def channel_removeowner(token, channel_id, u_id):
    server_data = get_data()
    
    # first get the u_id from the user token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    owner_uid = token_payload['u_id']
    
    to_remove = None
    # now check whether or not the channel actually exists, if it does exist
    # set it to a value and break out of the loop earlier
    for channel in server_data["channels"]:
        if channel._channel_id == channel_id:
            to_remove = channel
            break
    
    # if the channel requested does not exist or the u_id is not an owner of it
    # raise an error
    if to_remove == None:
        raise ValueError(description="The requested channel does not exist")
    
    if u_id not in to_remove._owners:
        raise ValueError(description="The user is not an owner of this channel")

    if owner_uid not in to_remove._owners:
        raise AccessError(description="You do not have permissions to do this")
    
    
    # finally remove the u_id as an owner of the channel requested, we will need
    # to interact with a database to handle this
    to_remove._owners.remove(u_id)

    return {}

