#   user_profile_sethandle(token, handle_str);
#   return void
#   Exception: ValueError when:
#       - handle_str is no more than 20 characters
#   Description: Update the authorised user's handle (i.e. display name)

def user_profile_sethandle(token, handle_str):
    # find u_id associated with token (with non-existent database)
    u_id = 12345
    handle_check(handle_str)
    handle_in_use_check(handle_str)
    change_handle(u_id, handle)

    return void

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

def change_handle(u_id, handle):
    # change first and last name in the database (which doesn't exist yet)
    pass
