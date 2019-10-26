import jwt
from .database import *
from .access_error import AccessError


def channels_list(token):
    # this is pretty simple, just grab the "database"
    database = get_data()

    # if the token is not valid throw an AccessError
    # (for now make it return True by default because
    # apparently we want everyone to be able to access
    # all the channels)
    if not database["tokens"].get(token, True):
        raise AccessError

    # get the user's u_id
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    channels = [
        c.frontend_format() for c in database["channels"] if u_id in c._members
    ]

    # quick little list comprehension to return the channels in the format
    # we need
    return { "channels" : channels }