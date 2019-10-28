import jwt
from .database import get_data, get_secret
from .access_error import *


#   user_profile_sethandle(token, handle_str);
#   return void
#   Exception: ValueError when:
#       - handle_str is no more than 20 characters
#   Description: Update the authorised user's handle (i.e. display name)

def user_profile_sethandle(token, handle_str):
    # find u_id associated with token (with non-existent database)
    u_id = check_valid_token(token)
    
    handle_check(handle_str)
    handle_in_use_check(handle_str)
    change_handle(u_id, handle_str)

    return


def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    DATABASE = get_data()
    SECRET = get_secret()
    token = jwt.decode(token, SECRET, algorithms=['HS256'])

    for x in DATABASE["users"]:
        user_id = x.get_u_id()
        if user_id == token["u_id"]:
            return user_id
    raise ValueError(description="token invalid")

        
def handle_check(handle_str):
    if len(handle_str) < 20 and len(handle_str) > 0:
        return True
    raise ValueError(description="Handle must be between 1 and 20 characters")


def handle_in_use_check(handle_str):
    # check if the handle is already being used/exists within the database
    DATABASE = get_data()

    for x in DATABASE["users"]:
        if x.get_handle() == handle_str:
            raise ValueError(description="Handle is already in use.")
    
    return True


def change_handle(u_id, handle_str):
    # change handle in the database for associated user
    DATABASE = get_data()
    
    for x in DATABASE["users"]:
        if x.get_u_id() == u_id:
            x.update_user_handle(handle_str)
            return True
    raise ValueError(description="Error: Couldn't change handle.")
