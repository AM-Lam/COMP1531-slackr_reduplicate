import hashlib
from .database import *


def auth_passwordreset_reset(reset_code, new_password):
    email = check_reset_code(reset_code)    # check if the reset code is valid and retrive the email
    if chec_password_strength(new_password) == True:    # is the password strong enough?
        for users in update_data['users']:  # finding the user in the list of users
            if users._email == email:       # looking for the user in the users list in the database.
                hashed_pass = (hashlib.sha256(new_password.encode()).hexdigest())   # hashing the new password
                users.update_user_password(hashed_pass)    # updating the old password
                del update_data["reset"][reset_code]    # once the password is updated, delete the reset_code, 
                                                        # so that it can not be used again.
    return {}
    

def check_reset_code(reset_code):
    # this will check if the reset code sent by the auth_passwordreset_request function is correct
    if reset_code in update_data['reset'].keys():
        email = update_data['reset'][reset_code]
        return email
    else:
        raise ValueError("reset code incorrect!")

def chec_password_strength(password):
    # to check if the password is at least 5 digits 
    if len(password) >= 5:
        return True
    else:
        raise ValueError("Password is too short!")