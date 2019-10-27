import re
import jwt
from .database import get_data, get_secret
from .access_error import *


#   user_profile_setemail(token, email);
#   return void
#   Exception: ValueError when:
#       - Email entered is not a valid email,
#       - Email address is already being used by another user
#   Description: Update the authorised user's email address

def user_profile_setemail(token, email):

    u_id = check_valid_token(token)
    check_if_email_valid(email)
    check_email_database(email)
    change_email(u_id, email)

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


def check_if_email_valid(email):
    # run the re module to identify if an email is valid
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, email)):
        return True
    raise ValueError(description="Email is invalid.")

def check_email_database(email):
    # check if the email is already being used/is within the database
    DATABASE = get_data()

    for x in DATABASE["users"]:
        if x.get_email() == email:
            raise ValueError(description="Email is already in use.")
    return True

def change_email(u_id, email):
    # change email in the database for the specified user
    DATABASE = get_data()
    
    for x in DATABASE["users"]:
        if x.get_u_id() == u_id:
            x.update_user_email(email)
            return True
    raise ValueError(description="Error: Couldn't change email.")
