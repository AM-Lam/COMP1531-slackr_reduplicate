"""
Functions that relate to the creation, modification and deletion of users.
"""

import urllib
import jwt
from .database import is_email_valid, check_email_database, check_valid_token, check_valid_token, get_data, get_user, is_handle_in_use
from .access_error import AccessError, Value_Error


def user_profile_setemail(token, email):
    """
    user_profile_setemail(token, email);
    return {}
    Exception: Value_Error when:
        - Email entered is not a valid email,
        - Email address is already being used by another user
    Description: Update the authorised user's email address
    """
    
    is_email_valid(email)
    check_email_database(email)
    
    u_id = check_valid_token(token)
    get_user(u_id).update_email(email)

    return {}


def user_profile_sethandle(token, handle_str):
    """
    user_profile_sethandle(token, handle_str);
    return void
    Exception: Value_Error when:
        - handle_str is no more than 20 characters
    Description: Update the authorised user's handle (i.e. display name)
    """
    
    if not 0 < len(handle_str) < 20:
        raise Value_Error(description="Handles must be between 0 and 20\
                         characters (exclusive)")

    if is_handle_in_use(handle_str):
        raise Value_Error(description="Handle is already in use")
    
    u_id = check_valid_token(token)
    get_user(u_id).update_handle(handle_str)

    return {}


def user_profile_setname(token, name_first, name_last):
    if not 0 < len(name_first) < 50:
        raise Value_Error(description="First name must be between 0 and 50\
                         characters (exclusive)")
    
    if not 0 <= len(name_last) < 50:
        raise Value_Error(description="Last name must be between 0 and 50\
                         characters (inclusive)")

    u_id = check_valid_token(token)
    user = get_user(u_id)
    
    user.update_first_name(name_first)
    user.update_last_name(name_last)

    return {}


def user_profile(token, u_id):
    server_data = get_data()

    # not a valid token
    if not server_data["tokens"].get(token, False):
        raise AccessError 

    if u_id in server_data["users"]:
        user = server_data["users"][u_id]

        return {
            "email" : user.get_email(),
            "name_first" : user.get_first_name(),
            "name_last" : user.get_last_name(),
            "handle_str" : user.get_handle()
        }
    
    raise Value_Error(description="User cannot be found")


def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end,     y_end):
    # find u_id associated with token (with non-existent database)
    #TODO: (note: this is not required to be completed until iteration 3)
    user_id = check_valid_token(token)

    # just to suppress the error form pylint
    assert user_id is not None

    check_imgurl(img_url)
    check_start_coords(x_start, y_start)
    check_end_coords(x_end, y_end)
    check_sequential(x_start, y_start, x_end, y_end)
    check_square(x_start, y_start, x_end, y_end)
    change_photo(img_url, x_start, y_start, x_end, y_end)
    
    return {}

        
def check_imgurl(img_url):
    if urllib.request.urlopen(img_url).getcode() == 200:
        return True
    raise Value_Error(description="The URL is not working at the moment!")


def check_start_coords(x_start, y_start):
    # we don't know how to get image dimensions yet, so we will assume the max image size is 200x200
    IMG_LIMIT = 200
    if x_start >= 0 and y_start >= 0 and x_start <= IMG_LIMIT and y_start <= IMG_LIMIT:
        return True
    raise Value_Error(description="Co-ordinates out of bounds.")


def check_end_coords(x_end, y_end):
    # we don't know how to get image dimensions yet, so we will assume the max image size is 200x200
    IMG_LIMIT = 200
    if x_end >= 0 and y_end >= 0 and x_end <= IMG_LIMIT and y_end <= IMG_LIMIT:
        return True
    raise Value_Error(description="Co-ordinates out of bounds.")


def check_sequential(x_start, y_start, x_end, y_end):
    # check if start is before end
    if x_start >= x_end or x_end <= x_start:
        raise Value_Error(description="Co-ordinates are not sequential.")
    if y_start >= y_end or y_end <- y_start:
        raise Value_Error(description="Co-ordinates are not sequential.")
    return True


def check_square(x_start, y_start, x_end, y_end):
    # usually profile pictures need to be square so we check if the co-ordinates match
    side1 = x_end - x_start
    side2 = y_end - y_start

    if side1 != side2:
        raise Value_Error(description="Co-ordinate selection is not a square.")
    return True


def change_photo(img_url, x_start, y_start, x_end, y_end):
    # change the photo in the database (which doesn't exist)
    pass

def users_all(token):
    userlist = []
    users_id = check_valid_token(token)
    # if the user exists then return a list of all the users!
    datab = get_data()["users"]
    # A value error will be raised if the user does not exist within the helper 
    # function.
    # All users need to be able to access this data to be able to invite other users.
    peep = datab[users_id]
    for key, value in datab.items():
        name_h = value.get_handle()
        userlist.append(name_h)

    return {'users':userlist}