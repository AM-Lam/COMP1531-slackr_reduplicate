"""
Functions to handle creating users and handling changes to passwords
"""

# pylint: disable=C0114
# pylint: disable=C0116

import time
import random
import hashlib
import string
import jwt
from .database import (is_email_valid, get_data, check_email_database,
                       get_secret, User, u_id_from_email, get_user,
                       u_id_from_email_reset, check_reset_code,
                       check_valid_token)
from .access_error import AccessError, Value_Error


def auth_login(email, password):
    # checking if the email has a valid structure.
    is_email_valid(email)

    # retriving the u_id if the password is correct and the email
    # exists
    u_id = u_id_from_email(email, password)

    # now we encode a unique token with the help of u_id and the
    # current time.
    token = jwt.encode({'u_id': u_id, 'time': time.time()}, get_secret(),
                       algorithm='HS256').decode()

    # adding the token to the list of tokens to be killed later
    get_data()["tokens"][token] = True

    return {"u_id": u_id, "token": token}


def auth_logout(token):
    update_data = get_data()

    # if the token is active
    if token in update_data["tokens"]:
        # deleting the token from existence.
        del update_data["tokens"][token]

        # now that the token has been deleted we return true
        return {'is_success' : True}

    raise Value_Error(description="Session token is already invalid")


def auth_passwordreset_request(email):
    update_data = get_data()

    # this checks if the givin email even exists and retrives id.
    user_id = u_id_from_email_reset(email)

    # send_code(email, userid, APP)

    # multiplying a random number to user id.
    random_num = user_id * (random.randint(1, 10000))

    # getting a random alphabet
    random_alph = random.choice(string.ascii_letters)

    # appending the two together
    random_str = str(random_num) + random_alph

    # hashing the code
    code = hashlib.sha256(random_str.encode()).hexdigest()

    # adding the code email combo to the database for future refrence.
    update_data["reset"][code] = email

    return code


def auth_passwordreset_reset(reset_code, new_password):
    update_data = get_data()

    # check if the reset code is valid and retrive the email
    email = check_reset_code(reset_code)

    if len(new_password) < 6:
        raise Value_Error(description="Passwords must be at least 6 characters\
                         in length")

    # find the user in the list of users
    for u_id in update_data['users']:
        # looking for the user in the users list in the database.
        user = get_user(u_id)
        if user.get_email() == email:
            # hash the new password
            hashed_pass = hashlib.sha256(new_password.encode()).hexdigest()

            # update the old password
            user.update_password(hashed_pass)

            # once the password is updated, delete the reset code
            del update_data["reset"][reset_code]

    return {}


def auth_register(email, password, first_name, last_name):
    update_data = get_data()

    if not 0 < len(first_name) < 50:
        raise Value_Error(description="First name must be between 0 and 50\
                         characters (exclusive)")

    if not 0 <= len(last_name) < 50:
        raise Value_Error(description="Last name must be between 0 and 50\
                         characters (inclusive)")

    # checking if password is strong and getting a hash.
    if len(password) < 6:
        raise Value_Error(description="Passwords must be at least 6 characters\
                         in length")

    password = hashlib.sha256(password.encode()).hexdigest()

    # checking if the email has a valid structure.
    is_email_valid(email)

    # checking if the email already exists.
    check_email_database(email)

    # getting the number of currently registered users.
    listlen = len(update_data['users'])

    # new user id is the number of current users plus one.
    u_id = listlen + 1

    # now we encode a unique token with the help of u_id and the current time.
    token = jwt.encode({'u_id': u_id, 'time': time.time()}, get_secret(),
                       algorithm='HS256').decode()

    # adding the token to the list of tokens to be killed later.
    update_data["tokens"][token] = True

    # creating a user class instance.
    person = User(u_id, first_name, last_name, password, email)

    # if this is the first user to register make them a slackr owner
    if u_id == 1:
        person.set_global_admin(True)
        person.set_slackr_owner(True)

    # adding the person to the user dictionary.
    update_data['users'][u_id] = person

    return {"u_id": u_id, "token": token}


def admin_userpermission_change(token, u_id, p_id):
    """
    admin_userpermission_change(token, u_id, permission_id);
    return {}
    Exception: Value_Error when:
        - u_id does not refer to a valid user,
        - permission_id does not refer to a value permission,
    AccessError when:
        - The authorised user is not an admin or owner
    Description: Given a User by their user ID, set their permissions to new permissions described by permission_id
    """

    # call the database
    server_data = get_data()

    # check if the token is valid and decode it
    request_u_id = check_valid_token(token)

    # attempt to find valid users for both the people giving and receiving perms
    request_user = None
    user = None
    for u in server_data["users"]:
        if u.get_u_id() == u_id:
            user = u
        if u.get_u_id() == request_u_id:
            request_user = u

    # raise a Value_Error if either user can't be found
    if user == None:
        raise Value_Error(description="u_id does not refer to a real user")
    elif request_user == None:
        raise Value_Error(description="Request does not come from a real user")

    # raise an AccessError if the requesting user cannot use this function
    if not (request_user.is_global_admin() or request_user.is_slackr_owner()):
        raise AccessError(description="You do not have permissions to do this")

    # raise a Value_Error if the given permission ID is not valid
    if not (1 <= p_id <= 3):
        raise Value_Error(description=f"{p_id} is not a valid permission id")
    
    # global admins cannot change the perms of slackr owners
    if not request_user.is_slackr_owner() and user.is_slackr_owner():
        raise AccessError(description="You do not have permissions to do this")

    # handle the perm changes
    if p_id == 1:
        # make the user a slackr owner, only other slackr owners can do this
        if not request_user.is_slackr_owner():
            raise AccessError(description="You do not have permissions to do this")
        user._slackr_owner = True
        user.set_global_admin(True)
    elif p_id == 2:
        # make the user a global admin, this should always be possible if we
        # reach this point
        user._slackr_owner = False
        user.set_global_admin(True)
    else:
        # make the user a regular member, this should also always be possible
        # if we reach this point
        user._slackr_owner = False
        user.set_global_admin(False)
    
    return {}
