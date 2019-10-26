import jwt

#   user_profile_setname(token, name_first, name_last);
#   return void
#   Exception: ValueError when:
#       - name_first is more than 50 characters,
#       - name_last is more than 50 characters
#   Description: Update the authorised user's first and last name

def user_profile_setname(token, name_first, name_last):
    # find u_id associated with token (with non-existent database)
    u_id = check_valid_token(token)
    first_name_check(name_first)
    last_name_check(name_last)
    change_names(u_id, name_first, name_last)

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

def first_name_check(name_first):
    # check if the first name is within length limits/if first name exists
    if len(name_first) < 50 and len(name_first) > 0:
        return True
    else:
        raise ValueError("First name must be between 1 and 50 characters.")

def last_name_check(name_last):
    # check if the last name is within length limits
    if len(name_last) < 50:
        return True
    else:
        raise ValueError("Last name cannot exceed 50 characters.")

def change_names(u_id, name_first, name_last):
    # change first and last name in the database for the associated user
    global DATABASE
    try:
        for x in DATABASE["users"]:
            y = x.get_user_data()
            if y.get("u_id") == u_id:
                DATABASE.update_user_data({"first_name": name_first, "last_name": name_last})
                break
    except Exception as e:
        raise ValueError("Error: Couldn't change name.")
