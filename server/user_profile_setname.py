#   user_profile_setname(token, name_first, name_last);
#   return void
#   Exception: ValueError when:
#       - name_first is more than 50 characters,
#       - name_last is more than 50 characters
#   Description: Update the authorised user's first and last name

def user_profile_setname(token, name_first, name_last):
    # find u_id associated with token (with non-existent database)
    u_id = 12345
    first_name_check(name_first)
    last_name_check(name_last)
    change_names(u_id, name_first, name_last)

    return void

def first_name_check(name_first):
    if len(name_first) < 50 and len(name_first) > 0:
        return True
    else:
        raise ValueError("First name must be between 1 and 50 characters.")

def last_name_check(name_last):
    if len(name_last) < 50:
        return True
    else:
        raise ValueError("Last name cannot exceed 50 characters.")

def change_names(u_id, name_first, name_last):
    # change first and last name in the database (which doesn't exist yet)
    pass
