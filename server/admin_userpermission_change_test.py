from admin_userpermission_change import admin_userpermission_change
from auth_register import register
import pytest

def test_admin_userpermission_change():
    user = register("valid@email.com", "12345", "John", "Doe")
    
    # this test should pass with no issue
    assert admin_userpermission_change(user["token"], 12345, 1) == None

    # if the user is invalid
    pytest.raises(ValueError, admin_userpermission_change, user["token"], 54321, 1)

    # if the permission is invalid
    pytest.raises(ValueError, admin_userpermission_change, user["token"], 12345, -1)

    # if the user is not an admin/owner
    # pytest.raises(AccessError, admin_userpermission_change, "badtoken", 12345, -1)
