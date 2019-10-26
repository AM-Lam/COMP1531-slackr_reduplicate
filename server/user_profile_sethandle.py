#   user_profile_sethandle(token, handle_str);
#   return void
#   Exception: ValueError when:
#       - handle_str is no more than 20 characters
#   Description: Update the authorised user's handle (i.e. display name)

def user_profile_sethandle(token, handle_str):
    # find u_id associated with token (with non-existent database)
    u_id = check_valid_token(token)
    
    handle_check(handle_str)
    handle_in_use_check(handle_str)
    change_handle(u_id, handle_str)

    return

def check_valid_token(token):
    global DATABASE
    # find the user ID associated with this token, else raise a ValueError
    try:
        for x in DATABASE:
            if x.get("token") == token:
                return x.get("u_id")
    except Exception as e:
        raise ValueError("token invalid")

def handle_check(handle_str):
    if len(handle_str) < 20 and len(handle_str) > 0:
        return True
    else:
        raise ValueError("Handle must be between 1 and 20 characters")

def handle_in_use_check(handle_str):
    # check if the handle is already being used/exists within the database
    global DATABASE
    for x in DATABASE["handle"]:
        if x.get("handle") == handle_str:
            raise ValueError("Handle is already in use.")
    return True

def change_handle(u_id, handle_str):
    # change handle in the database for associated user
    global DATABASE
    try:
        for x in DATABASE["users"]:
            if x.get("u_id") == u_id:
                DATABASE.update_user_data({"handle": handle})
    except Exception as e:
        raise ValueError("Error: Couldn't change handle.")
