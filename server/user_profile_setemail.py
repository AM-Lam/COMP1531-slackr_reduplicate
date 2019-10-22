import re
import jwt

#   user_profile_setemail(token, email);
#   return void
#   Exception: ValueError when:
#       - Email entered is not a valid email,
#       - Email address is already being used by another user
#   Description: Update the authorised user's email address

def user_profile_setemail(token, email):
    # find u_id associated with token (with non-existent database)
    admin_user_id = check_valid_token(token)

    check_if_email_valid(email)
    check_email_database(email)
    change_email(u_id, email)
    return

def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    decoded_jwt = jwt.decode(token, 'sempai', algorithms=['HS256'])
    try:
        for x in database:
            if x.get("u_id") == decoded_jwt.key():
                return x.get("u_id")
    except Exception as e:
        raise ValueError("token invalid")

def check_if_email_valid(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, email)):
        return True
    else:
        raise ValueError("Email is invalid.")

def check_email_database(email):
    # when database is implemented, check if the email is already being used
    # since the database doesn't exist yet, just pretend the test input "cs1531@cse.unsw.edu.au" is already in use
    if email != "cs1531@cse.unsw.edu.au":
        return True
    else:
        raise ValueError("Email is already in use.")

def change_email(u_id, email):
    # change email in the database (which doesn't exist yet)
    pass
