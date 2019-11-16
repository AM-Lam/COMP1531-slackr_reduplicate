"""
Functions that relate to the creation, modification and deletion of users.
"""

# pylint: disable=R0913
# pylint: disable=W0613

import urllib
import jwt
from PIL import Image
from .database import (is_email_valid, check_email_database, check_valid_token,
                       get_data, get_user, is_handle_in_use)
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
    Exception: Value_Error when:
        - handle_str is no more than 20 characters
    Description: Update the authorised user's handle (i.e. display name)
    """

    # check if the handle passes length requirements
    if not 0 < len(handle_str) < 20:
        raise Value_Error(description="Handles must be between 0 and 20\
                         characters (exclusive)")

    # check the database for handles in use
    if is_handle_in_use(handle_str):
        raise Value_Error(description="Handle is already in use.")

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # call a database method that changes the profile handle
    get_user(u_id).update_handle(handle_str)

    return {}


def user_profile_setname(token, name_first, name_last):
    """
    user_profile_setname(token, name_first, name_last);
    return {}
    Exception: Value_Error when:
        - name_first is more than 50 characters,
        - name_last is more than 50 characters
    Description: Update the authorised user's first and last name
    """

    # check if the first name passes length requirements
    if not 0 < len(name_first) < 50:
        raise Value_Error(description="First name must be between 0 and 50\
                         characters (exclusive)")

    # check if the last name passes length requirements
    if not 0 <= len(name_last) < 50:
        raise Value_Error(description="Last name must be between 0 and 50\
                         characters (inclusive)")

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # grab the users details from the database
    user = get_user(u_id)

    # call a database method that changes both profile names
    user.update_first_name(name_first)
    user.update_last_name(name_last)

    return {}


def user_profile(token, u_id, live_str=""):
    """
    Taking a u_id return the user data of its associated user, if the
    user does not exist raise a Value_Error. live_str is a string repre
    -senting the localhost when we are live, during testing it should
    not be touched
    """

    server_data = get_data()

    # not a valid token
    if not server_data["tokens"].get(token, False):
        raise AccessError

    if u_id in server_data["users"]:
        user = server_data["users"][u_id]

        return {
            "u_id" : u_id,
            "email" : user.get_email(),
            "name_first" : user.get_first_name(),
            "name_last" : user.get_last_name(),
            "handle_str" : user.get_handle(),
            "profile_img_url" : live_str + user.get_profile_img_url()
        }

    raise Value_Error(description="User cannot be found")


def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """
    user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end,
                              y_end);
    return {}
    Exception: Value_Error when:
        - img_url is returns an HTTP status other than 200,
        - x_start, y_start, x_end, y_end are all within the dimensions
          of the image at the URL.
    Description: Given a URL of an image on the internet, crops the
        image within bounds (x_start, y_start) and (x_end, y_end).
        Position (0,0) is the top left.
    """

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # just to suppress the error from pylint
    assert u_id is not None

    # check that the URL is actually open for reading
    if urllib.request.urlopen(img_url).getcode() != 200:
        raise Value_Error(description="The URL is not working at the moment!")

    local_filename, _ = urllib.request.urlretrieve(img_url)
    image_object = Image.open(local_filename)

    # set the max size of the image to the smaller of the
    # image's own dimensions
    img_limit = min(image_object.size)

    if image_object.format.lower() not in ["jpeg", "jpg"]:
        raise Value_Error(description="Invalid file type.")

    # check if the start co-ordinates are valid
    if not 0 <= x_start < img_limit or not 0 <= y_start < img_limit:
        raise Value_Error(description="Start co-ordinates out of bounds.")

    # check if the end co-ordinates are valid
    if not 0 < x_end <= img_limit or not 0 < y_end <= img_limit:
        raise Value_Error(description="End co-ordinates out of bounds.")

    # check if co-ordinates are sequential
    if x_start >= x_end or y_start >= y_end:
        raise Value_Error(description="Co-ordinates are not sequential.")

    # check if the image selection is a square
    side1 = x_end - x_start
    side2 = y_end - y_start
    
    if side1 != side2:
        raise Value_Error(description="Co-ordinate selection is not a square.")

    cropped = image_object.crop((x_start, y_start, x_end, y_end))

    img_url = f'static/profile_images/{u_id}.jpg'
    cropped.save(img_url, "JPEG")

    get_user(u_id).set_profile_img_url(img_url)
    
    return {}



def users_all(token, live_str=""):
    # live_str is a string that represents the path to the server
    # when live, during testing it should be blank

    # ensure that this is a valid token, we don't need the u_id as
    # all users can access this
    check_valid_token(token)

    user_list = []
    for u_id in get_data()["users"]:
        user_list.append(user_profile(token, u_id, live_str))
    
    print(user_list)
    return {"users" : user_list}
