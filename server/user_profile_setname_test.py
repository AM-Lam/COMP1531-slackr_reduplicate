import pytest
from .user_profile_setname import user_profile_setname
from .auth_register import auth_register
from .access_error import AccessError

def test_user_profile_setname():
    user = auth_register("valid@email.com", "123456", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_setname(user["token"], "Jane", "Smith") == None

    # trying to input a first name longer than 50 characters
    pytest.raises(ValueError, user_profile_setname, user["token"], "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "Smith")

    # trying to input a last name longer than 50 characters
    pytest.raises(ValueError, user_profile_setname, user["token"], "Jane", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")

    # assuming we allow mononymous names, at least one value needs to be filled
    assert user_profile_setname(user["token"], "Plato", "") == None

    # trying to input an empty name
    pytest.raises(ValueError, user_profile_setname, user["token"], "", "")
