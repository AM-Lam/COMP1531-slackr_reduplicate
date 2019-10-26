import jwt
from .database import *
from .access_error import *


def channel_leave(token, channel_id):
    # somehow get the associated uid, this will presumably need
    # to interact with a database or something similar
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    server_data = get_data()

    # try to remove the user from the channel, if they are not in the
    # channel then just return without any error
    channel_exists = False
    for c in server_data["channels"]:
        if c._channel_id == channel_id:
            if u_id in c._members:
                c._members.remove(u_id)
            return {}
    
    # if we get here the channel does not exist and we need to raise an
    # exception
    raise ValueError

