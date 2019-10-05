from user_profile_sethandle import user_profile_sethandle
from auth_register import auth_register
import pytest

def test_user_profile_sethandle():
    user = auth_register("valid@email.com", "12345", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_sethandle(user["token"], "handle") == None

    # return a ValueError if the handle is too long
    pytest.raises(ValueError, user_profile_sethandle, user["token"], "abcdefghijklmnopqrstuvwxyz")

    # if the handle (tested by "handle1") is already in use
    pytest.raises(ValueError, user_profile_sethandle, user["token"], "handle1")
