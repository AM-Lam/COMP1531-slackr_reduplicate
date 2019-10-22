import jwt

#   user_profile_sethandle(token, handle_str);
#   return void
#   Exception: ValueError when:
#       - handle_str is no more than 20 characters
#   Description: Update the authorised user's handle (i.e. display name)

def user_profile_sethandle(token, handle_str):
    # find u_id associated with token (with non-existent database)
    admin_user_id = check_valid_token(token)
    
    handle_check(handle_str)
    handle_in_use_check(handle_str)
    change_handle(u_id, handle_str)

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

def handle_check(handle_str):
    if len(handle_str) < 20 and len(handle_str) > 0:
        return True
    else:
        raise ValueError("Handle must be between 1 and 20 characters")

def handle_in_use_check(handle_str):
    # when database is implemented, check if the handle is already being used
    # since the database doesn't exist yet, just pretend the test input "handle1" is already in use
    if handle_str != "handle1":
        return True
    else:
        raise ValueError("Handle is already in use.")

def change_handle(u_id, handle_str):
    # change first and last name in the database (which doesn't exist yet)
    pass
