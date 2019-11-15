from .access_error import AccessError, ValueError
from .database import *
import jwt
from .access_error import *
from .database import *

#   user_profile_setname(token, name_first, name_last);
#   return void
#   Exception: ValueError when:
#       - name_first is more than 50 characters,
#       - name_last is more than 50 characters
#   Description: Update the authorised user's first and last name

def user_profile_setname(token, name_first, name_last):
    # find u_id associated with token (with non-existent database)
    u_id = check_valid_token(token)

    first_name_check(name_first)
    last_name_check(name_last)
    change_names(u_id, name_first, name_last)

    return

def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    DATABASE = get_data()
    SECRET = get_secret()
    token = jwt.decode(token, SECRET, algorithms=['HS256'])

    try:
        for x in DATABASE["users"]:
            user_id = x.get_u_id()
            if user_id == token["u_id"]:
                return user_id
    except Exception as e:
        raise ValueError(description="token invalid")

def first_name_check(name_first):
    # check if the first name is within length limits/if first name exists
    if len(name_first) < 50 and len(name_first) > 0:
        return True
    else:
        raise ValueError(description="First name must be between 1 and 50 characters.")

def last_name_check(name_last):
    # check if the last name is within length limits
    if len(name_last) < 50:
        return True
    else:
        raise ValueError(description="Last name cannot exceed 50 characters.")

def change_names(u_id, name_first, name_last):
    # change first and last name in the database for the associated user
    DATABASE = get_data()
    
    try:
        for x in DATABASE["users"]:
            y = x.get_user_data()
            if y.get("u_id") == u_id:
                x.update_user_first_name(name_first)
                x.update_user_last_name(name_last)
                return True
    except Exception as e:
        raise ValueError(description="Error: Couldn't change name.")
