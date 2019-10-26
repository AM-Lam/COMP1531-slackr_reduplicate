import pytest
from .user_profile_sethandle import user_profile_sethandle
from .auth_register import auth_register
from .access_error import *
from .database import *


clear_data()


def test_user_profile_sethandle():
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_sethandle(user["token"], "handle") == None

    # return a ValueError if the handle is too long
    pytest.raises(ValueError, user_profile_sethandle, user["token"], "abcdefghijklmnopqrstuvwxyz")

    # if the handle (tested by "handle1") is already in use
    pytest.raises(ValueError, user_profile_sethandle, user["token"], "handle1")
