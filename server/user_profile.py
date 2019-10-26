import jwt
from .database import *
from .access_error import AccessError

def user_profile(token, u_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    check_u_id = token_payload["u_id"]

    # not an authorised user
    if token not in server_data['token']:
        raise AccessError 

    # authorization problem
    if check_u_id != u_id:
            raise ValueError
    
    for info in server_data['users']:
        if info._u_id == u.id:
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
            raise ValueError
    