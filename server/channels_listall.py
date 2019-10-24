from .database import *
from .access_error import AccessError


def channels_listall(token):
    # this is pretty simple, just grab the "database"
    database = get_data()

    # if the token is not valid throw an AccessError
    # (for now make it return True by default because
    # apparently we want everyone to be able to access
    # all the channels)
    if not database["tokens"].get(token, True):
        raise AccessError

    # quick little list comprehension to return the channels in the format
    # we need
    return { "channels" : [c.frontend_format() for c in database["channels"]] }
