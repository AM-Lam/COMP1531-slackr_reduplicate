"""
Functions that relate to the creation, modification and deletion of users.
"""

import urllib
import jwt
from .database import *
from .access_error import *
from PIL import Image


def user_profile_setemail(token, email):
    """
    user_profile_setemail(token, email);
    return {}
    Exception: ValueError when:
        - Email entered is not a valid email,
        - Email address is already being used by another user
    Description: Update the authorised user's email address
    """

    # check if the email is valid and not already in use
    is_email_valid(email)
    check_email_database(email)

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # call a database method that changes the profile email
    get_user(u_id).update_email(email)

    return {}

def user_profile_sethandle(token, handle_str):
    """
    user_profile_sethandle(token, handle_str);
    return void
    Exception: ValueError when:
        - handle_str is no more than 20 characters
    Description: Update the authorised user's handle (i.e. display name)
    """

    # check if the handle passes length requirements
    if not 0 < len(handle_str) < 20:
        raise ValueError(description="Handles must be between 0 and 20\
                         characters (exclusive)")

    # check the database for handles in use
    if is_handle_in_use(handle_str):
        raise ValueError(description="Handle is already in use.")

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # call a database method that changes the profile handle
    get_user(u_id).update_handle(handle_str)

    return {}

def user_profile_setname(token, name_first, name_last):
    """
    user_profile_setname(token, name_first, name_last);
    return {}
    Exception: ValueError when:
        - name_first is more than 50 characters,
        - name_last is more than 50 characters
    Description: Update the authorised user's first and last name
    """

    # check if the first name passes length requirements
    if not 0 < len(name_first) < 50:
        raise ValueError(description="First name must be between 0 and 50\
                         characters (exclusive)")

    # check if the last name passes length requirements
    if not 0 <= len(name_last) < 50:
        raise ValueError(description="Last name must be between 0 and 50\
                         characters (inclusive)")

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # grab the users details from the database
    user = get_user(u_id)

    # call a database method that changes both profile names
    user.update_first_name(name_first)
    user.update_last_name(name_last)

    return {}

def user_profile(token, u_id):
    server_data = get_data()

    # not a valid token
    if not server_data["tokens"].get(token, False):
        raise AccessError 
    
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

######################################################################################

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end,     y_end):
    """
    user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end,     y_end);
    return {}
    Exception: ValueError when:
        - img_url is returns an HTTP status other than 200,
        - x_start, y_start, x_end, y_end are all within the                   dimensions of the image at the URL.
    Description: Given a URL of an image on the internet, crops the image within bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
    """

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # just to suppress the error form pylint
    assert u_id is not None

    # check that the URL is actually open for reading
    if urllib.request.urlopen(img_url).getcode() != 200:
        raise ValueError(description="The URL is not working at the moment!")

    im = Image.open(img_url)
    IMG_LIMIT = min(im.size)

    # TODO: Check if the image is a valid file
    if im.info["filetype"] != JPEG:
        raise ValueError(description="Invalid file type.")

    # check if the start co-ordinates are valid
    if x_start < 0 or y_start < 0 or x_start >= IMG_LIMIT or y_start >= IMG_LIMIT:
        raise ValueError(description="Start co-ordinates out of bounds.")

    # check if the end co-ordinates are valid
    if x_end <= 0 or y_end <= 0 and x_end > IMG_LIMIT and y_end > IMG_LIMIT:
        raise ValueError(description="End co-ordinates out of bounds.")

    # check if co-ordinates are sequential
    if x_start >= x_end or x_end <= x_start or y_start >= y_end or y_end <= y_start:
        raise ValueError(description="Co-ordinates are not sequential.")

    # check if the image selection is a square
    side1 = x_end - x_start
    side2 = y_end - y_start
    if side1 != side2:
        raise ValueError(description="Co-ordinate selection is not a square.")

    local_filename, headers = urllib.request.urlretrieve(img_url)

    imageObject = Image.open(local_filename)
    cropped = imageObject.crop(x_start, y_start, x_end, y_end)
    cropped.save(u_id + ".jpg", "JPEG")

    get_user(u_id).set_profile_img_url(cropped)
    
    return {}
