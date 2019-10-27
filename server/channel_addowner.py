import jwt
from .database import *
from .access_error import *
from .channels_list import channels_list


def channel_addowner(token, channel_id, u_id):
    server_data = get_data()

    # first check whether or not the token is valid, since auth_register is not
    # yet complete just always pass this test
    if not server_data["tokens"].get(token, False):
        raise AccessError("Token not valid")

    # first get the u_id from the user token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    owner_u_id = token_payload["u_id"]

    to_add = None
    # now check whether or not the channel actually exists, if it does exist
    # set it to a value and break out of the loop earlier
    for channel in server_data["channels"]:
        if channel._channel_id == channel_id:
            to_add = channel
            break

    # if the channel requested does not exist or the u_id is already an owner of
    # it raise an error, this will probably need to interact with a database
    if to_add == None:
        raise ValueError(description="The channel requested does not exist")
    
    if u_id in channel._owners:
        raise ValueError(description="The user is already an owner in this channel")

    # now make sure the calling user has the permissions to make this change, we
    # will need a few functions to be written that access a database for this to
    # work
    if owner_u_id not in channel._owners:
       raise AccessError(description="Lack permissions to add owner to this channel")

    # finally set the u_id to be an owner of the channel requested
    channel._owners.append(u_id)
    if u_id not in channel._members:
        channel._members.append(u_id)

    return {}
