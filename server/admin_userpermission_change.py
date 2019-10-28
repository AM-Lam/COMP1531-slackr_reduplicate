import jwt
from .access_error import *
from .database import *

#   admin_userpermission_change(token, u_id, permission_id);
#   return void
#   Exception: ValueError when:
#       - u_id does not refer to a valid user,
#       - permission_id does not refer to a value permission,
#   AccessError when:
#       - The authorised user is not an admin or owner
#   Description: Given a User by their user ID, set their permissions to new permissions described by permission_id

def admin_userpermission_change(token, u_id, permission_id):

    admin_user_id = check_valid_token(token)
    check_valid_user(u_id)
    check_valid_permission(permission_id)
    check_owner_or_admin(admin_user_id)
    change_permission(u_id, permission_id)
    
    return

def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    DATABASE = get_data()
    SECRET = get_secret()
    token = jwt.decode(token, SECRET, algorithms=['HS256'])

    try:
        for x in DATABASE["users"]:
            user_id = x.get_u_id()
            if user_id == token["u_id"]:
                return user_id
    except Exception as e:
        raise ValueError(description="token invalid")

def check_valid_user(u_id):
    # check if the u_id given currently exists within the global database
    DATABASE = get_data()

    try:
        for x in DATABASE["users"]:
            y = x.get_user_data()
            if y.get("u_id") == u_id:
                return True
    except Exception as e:
        raise ValueError(description="This user does not exist.")

def check_valid_permission(permission_id):
    # assuming that 0 = user, 1 = admin, 2 = owner
    if permission_id < 0 or permission_id > 2:
        raise ValueError(description="Permission does not exist.")
    else:
        return True

def check_owner_or_admin(admin_user_id):
    # check if the permission_id associated with the user is an admin or owner
    DATABASE = get_data()

    try:
        for x in DATABASE["users"]:
            if admin_user_id == x.get_u_id():
                if x.is_global_admin == True:
                    return True
                elif x.is_global_admin == False:
                    raise AccessError("User is not an administrator.")
        raise AccessError("User does not have prerequisite permissions.")
    except Exception as e:
        raise ValueError(description="Could not access user permissions.")

def change_permission(u_id, permission_id):
    # change global permissions for user in the global database
    DATABASE = get_data()
    
    try:
        for x in DATABASE["channels"]:
            y = x.get_channel_data()
            if y.get("u_id") == u_id:
                x.add_owner(u_id)
    except Exception as e:
        raise ValueError(description="Error: Couldn't change permissions.")

