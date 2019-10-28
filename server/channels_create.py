from .database import *
from .access_error import *
import jwt


def channels_create(token, name, is_public):
    # first check for a valid name
    if len(name) > 20:
        raise ValueError(description="Channel name is too short")
    
    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]
    
    server_data = get_data()

    print(server_data)

    # make our channel id just be the count of channels we already have
    # incremented by 1, this way the channel_ids will increase sequentially
    channel_id = len(server_data["channels"]) + 1

    # at the start there will be no messages and the only member will be
    # the creator of the channel
    new_channel = Channel(channel_id, name, [], [u_id], is_public)
    
    # add the channel to the server database
    server_data["channels"].append(new_channel)

    # return the new channel's id
    return { "channel_id" : channel_id }
