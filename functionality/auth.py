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
                       u_id_from_email_reset, check_reset_code)
from .access_error import Value_Error


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
