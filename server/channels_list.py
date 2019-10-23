import jwt
from .access_error import AccessError
from .database import *


def channels_list(token):
    server_data = get_data()

    if not server_data["tokens"].get(token, False):
        raise AccessError

    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    channels = [ c.frontend_format() for c in server_data["channels"]
                if u_id in c._members ]
    
    return { "channels" : channels }
