from .access_error import AccessError
import re
import jwt

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
    global DATABASE
    global SECRET

    token = jwt.decode(token, SECRET, algorithms=['HS256'])

    try:
        for x in DATABASE["users"]:
            y = x.get_user_data()
            if y.get("u_id") == token["u_id"]:
                return y.get("u_id")
    except Exception as e:
        raise ValueError("token invalid")

def check_if_email_valid(email):
    # run the re module to identify if an email is valid
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, email)):
        return True
    else:
        raise ValueError("Email is invalid.")

def check_email_database(email):
    # check if the email is already being used/is within the database
    global DATABASE
    for x in DATABASE["email"]:
        y = x.get_user_data()
        if y.get("email") == email:
            raise ValueError("Email is already in use.")
    return True

def change_email(u_id, email):
    # change email in the database for the specified user
    global DATABASE
    try:
        for x in DATABASE["users"]:
            y = x.get_user_data()
            if y.get("u_id") == u_id:
                DATABASE.update_user_data({"email": handle})
                break
    except Exception as e:
        raise ValueError("Error: Couldn't change email.")
