"""
Function that allows an admin to change the permission's of users
"""


from .access_error import AccessError, Value_Error
from .database import get_data, get_user, check_valid_token


def admin_userpermission_change(token, u_id, p_id):
    """
    admin_userpermission_change(token, u_id, permission_id);
    return void
    Exception: Value_Error when:
        - u_id does not refer to a valid user,
        - permission_id does not refer to a value permission,
    AccessError when:
        - The authorised user is not an admin or owner
    Description: Given a User by their user ID, set their permissions
    to new permissions described by permission_id
    """
    server_data = get_data()

    if not server_data["tokens"].get(token, False):
        raise AccessError(description="Invalid token")


    request_u_id = check_valid_token(token)
    request_user = get_user(request_u_id)
    user = get_user(u_id)

    if user is None:
        raise Value_Error(description="u_id does not refer to a real user")

    if request_user is None:
        raise Value_Error(description="Request does not come from a real user")

    if not (request_user.is_global_admin() or request_user.is_slackr_owner()):
        raise AccessError(description="You do not have permissions to do this")

    if not 1 <= p_id <= 3:
        raise Value_Error(description=f"{p_id} is not a valid permission id")

    # global admins cannot change the perms of slackr owners
    if not request_user.is_slackr_owner() and user.is_slackr_owner():
        raise AccessError(description="You do not have permissions to do this")

    # handle the perm changes
    if p_id == 1:
        # make the user a slackr owner, only other slackr owners can do this
        if not request_user.is_slackr_owner():
            raise AccessError(description="You do not have permissions to do this")
        user.set_slackr_owner(True)
        user.set_global_admin(True)
    elif p_id == 2:
        # make the user a global admin, this should always be possible if we
        # reach this point
        user.set_slackr_owner(False)
        user.set_global_admin(True)
    else:
        # make the user a regular member, this should also always be possible
        # if we reach this point
        user.set_slackr_owner(False)
        user.set_global_admin(False)

    return {}
