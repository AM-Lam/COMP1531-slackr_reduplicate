import pytest
from .database import clear_data
from .access_error import *
from .admin_userpermission_change import admin_userpermission_change
from .auth_register import auth_register


def test_admin_userpermission_change():
    clear_data()
    
    user1 = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "Bob", "Doe")
    user3 = auth_register("valid3@email.com", "1234567890", "Jane", "Doe")
    user4 = auth_register("valid4@email.com", "1234567890", "Jen", "Doe")

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
    pytest.raises(ValueError, admin_userpermission_change, user2["token"], 666, 3)

    # try to change to a permision_id that is invalid (too low), this should
    # fail
    pytest.raises(ValueError, admin_userpermission_change, user2["token"], user4["u_id"], 0)

    # try to change to a permision_id that is invalid (too high), this should
    # fail
    pytest.raises(ValueError, admin_userpermission_change, user2["token"], user4["u_id"], 4)
