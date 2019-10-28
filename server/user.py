"""
Functions that relate to the creation, modification and deletion of users.
"""

import urllib
import jwt
from .database import get_data, get_secret, check_email_database, check_valid_token, handle_in_use_check
from .access_error import *


def user_profile_setemail(token, email):

    u_id = check_valid_token(token)
    check_if_email_valid(email)
    check_email_database(email)
    change_email(u_id, email)

    return {}


def user_profile_sethandle(token, handle_str):
    # find u_id associated with token
    u_id = check_valid_token(token)
    
    handle_check(handle_str)
    handle_in_use_check(handle_str)
    change_handle(u_id, handle_str)

    return {}


def user_profile_setname(token, name_first, name_last):
    # find u_id associated with token
    u_id = check_valid_token(token)
    first_name_check(name_first)
    last_name_check(name_last)
    change_names(u_id, name_first, name_last)

    return {}


def user_profile(token, u_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    check_u_id = token_payload["u_id"]

    # not an authorised user
    if not server_data["tokens"].get(token, False):
        raise AccessError 

    # authorization problem
    if check_u_id != u_id:
        raise ValueError(description="Invalid user")
    
    for info in server_data['users']:
        if info.get_u_id() == u_id:
            email = info.get_email()
            first_name = info.get_first_name()
            last_name = info.get_last_name()
            handle = info.get_handle()
            
            return { 
                'email': email,
                'name_first': first_name,
                'name_last': last_name,
                'handle_str': handle 
            }
    raise ValueError(description="User cannot be found")


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
    raise ValueError(description="The URL is not working at the moment!")


def check_start_coords(x_start, y_start):
    # we don't know how to get image dimensions yet, so we will assume the max image size is 200x200
    IMG_LIMIT = 200
    if x_start >= 0 and y_start >= 0 and x_start <= IMG_LIMIT and y_start <= IMG_LIMIT:
        return True
    raise ValueError(description="Co-ordinates out of bounds.")


def check_end_coords(x_end, y_end):
    # we don't know how to get image dimensions yet, so we will assume the max image size is 200x200
    IMG_LIMIT = 200
    if x_end >= 0 and y_end >= 0 and x_end <= IMG_LIMIT and y_end <= IMG_LIMIT:
        return True
    raise ValueError(description="Co-ordinates out of bounds.")


def check_sequential(x_start, y_start, x_end, y_end):
    # check if start is before end
    if x_start >= x_end or x_end <= x_start:
        raise ValueError(description="Co-ordinates are not sequential.")
    if y_start >= y_end or y_end <- y_start:
        raise ValueError(description="Co-ordinates are not sequential.")
    return True


def check_square(x_start, y_start, x_end, y_end):
    # usually profile pictures need to be square so we check if the co-ordinates match
    side1 = x_end - x_start
    side2 = y_end - y_start

    if side1 != side2:
        raise ValueError(description="Co-ordinate selection is not a square.")
    return True


def change_photo(img_url, x_start, y_start, x_end, y_end):
    # change the photo in the database (which doesn't exist)
    pass
