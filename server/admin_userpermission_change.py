import jwt

#   admin_userpermission_change(token, u_id, permission_id);
#   return void
#   Exception: ValueError when:
#       - u_id does not refer to a valid user,
#       - permission_id does not refer to a value permission,
#   AccessError when:
#       - The authorised user is not an admin or owner
#   Description: Given a User by their user ID, set their permissions to new permissions described by permission_id

def admin_userpermission_change(token, u_id, permission_id):
    # find u_id associated with token (with non-existent database)
    admin_user_id = check_valid_token(token)

    check_valid_user(u_id)
    check_valid_permission(permission_id)
    check_owner_or_admin(admin_user_id)
    change_permission(u_id, permission_id)
    
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

def check_valid_user(u_id):
    # currently we cannot check if u_ids are valid users so this just satisfies a rudimentary case
    try:
        for x in database:
            if x.get("u_id") == u_id:
                return True
    except Exception as e:
        raise ValueError("This user does not exist.")

def check_valid_permission(permission_id):
    # assuming that 0 = user, 1 = admin, 2 = owner
    if permission_id < 0 or permission_id > 2:
        raise ValueError("Permission does not exist.")
    else:
        return True

def check_owner_or_admin(token):
    # we need to check if the permission_id associated with the token is an admin or owner
    try:
        for x in database:
            if x.get("u_id") == token:
                check_perm = x["permissions"]

    if check_perm < 1:
        raise AccessError("User cannot undertake this action.")
    else:
        return True

def change_permission(u_id, permission_id):
   try:
    for x in database:
        if x.get("u_id") == u_id:
            x.["permissions"] = permission_id
