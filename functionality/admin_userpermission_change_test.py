# pylint: disable=C0114
# pylint: disable=C0116

import pytest
from .database import clear_data
from .access_error import AccessError, Value_Error
from .admin_userpermission_change import admin_userpermission_change
from .decorators import setup_data
from .auth import auth_register

# check if the basic functionality of message_send works or not
@setup_data(user_num=4)
def test_admin_userpermission_change(users, channels):

    user1 = users[0]
    user2 = users[1]    
    user3 = users[2]
    user4 = users[3]
    # as a slackr owner attempt to make a member an admin
    assert admin_userpermission_change(user1["token"], user2["u_id"], 2) == {}

    # as an admin attempt to make a member an admin
    assert admin_userpermission_change(user2["token"], user3["u_id"], 2) == {}

    # as an admin try to make a slackr owner a member, this should fail
    pytest.raises(AccessError, admin_userpermission_change, user2["token"], user1["u_id"], 3)

    # as an admin try to make an admin a slackr owner, this should fail
    pytest.raises(AccessError, admin_userpermission_change, user2["token"], user3["u_id"], 1)

    # as a regular member try to change somebody's perms, this should fail
    pytest.raises(AccessError, admin_userpermission_change, user4["token"], user3["u_id"], 3)

    # try to run with an invalid token
    pytest.raises(AccessError, admin_userpermission_change, 000, user3["u_id"], 1)

    # try to run with a user that does not exist
    pytest.raises(Value_Error, admin_userpermission_change, user2["token"], 666, 3)

    # try to change to a permision_id that is invalid (too low), this should
    # fail
    pytest.raises(Value_Error, admin_userpermission_change, user2["token"], user4["u_id"], 0)

    # try to change to a permision_id that is invalid (too high), this should
    # fail
    pytest.raises(Value_Error, admin_userpermission_change, user2["token"], user4["u_id"], 4)
