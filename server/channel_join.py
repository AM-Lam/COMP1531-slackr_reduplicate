import jwt
from .database import *
from .access_error import *
from .channels_listall import channels_listall


def channel_join(token, channel_id):
    server_data = get_data()
    # first try to get the relevant u_id from the provided token, this will need
    # us to interact with a database and retrieve data presumably
    
    # if the token is invalid throw an access error, since auth_register is not
    # complete just assume all tokens are valid
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")


    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]
    
    # next we have to check whether or not the given user is an admin, again
    # we'll probably need to interact with a db for this
    # is_admin = user_is_admin(u_id)
    found_channel = False

    for channel in server_data["channels"]:
        # somehow check if the channel is private, another database interaction
        # it should probably look like what's below
        if channel._channel_id == channel_id:
            if not channel._public: # we currently have no checks for global admins
                raise AccessError("Cannot join private channel as regular user")
            else:
                found_channel = True
                break

    if not found_channel:
        raise ValueError

    # add the user's u_id to the channel's list of members, since the data we 
    # get using channels_listall appears to be read-only
    channel._members.append(u_id)
    
    return {}    
    
