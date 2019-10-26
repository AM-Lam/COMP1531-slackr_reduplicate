from .database import *
from .admin_userpermission_change import admin_userpermission_change
from .auth_register import auth_register
from .access_error import AccessError
import pytest


clear_data()


def test_admin_userpermission_change():
    user = auth_register("valid@email.com", "12345", "John", "Doe")
    
    # this test should pass with no issue
    assert admin_userpermission_change(user["token"], 12345, 1) == None

    # if the user is invalid
    pytest.raises(ValueError, admin_userpermission_change, user["token"], 54321, 1)

    # if the permission is invalid
    pytest.raises(ValueError, admin_userpermission_change, user["token"], 12345, -1)

    pytest.raises(ValueError, admin_userpermission_change, user["token"], 12345, 3)

    # if the user is not an admin/owner
    pytest.raises(AccessError, admin_userpermission_change, "badtoken", 12345, -1)
