import jwt
from .database import *
from .access_error import *


def user_profile(token, u_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    check_u_id = token_payload["u_id"]

    # not an authorised user
    if not server_data["tokens"].get(token, True):
        raise AccessError 

    # authorization problem
    if check_u_id != u_id:
            raise ValueError(description="Invalid user")
    
    for info in server_data['users']:
        if info._u_id == u_id:
            email = info._email
            first_name = info._first_name
            last_name = info._last_name
            handle = info._handle
            
            return { 
                'email': email,
                'name_first': first_name,
                'name_last': last_name,
                'handle_str': handle 
            }
        # details cannot be found based on u_id
        else:
            raise ValueError(description="User cannot be found")
    
