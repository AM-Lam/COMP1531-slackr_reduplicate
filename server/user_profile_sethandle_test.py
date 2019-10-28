import pytest
from .user_profile_sethandle import user_profile_sethandle
from .auth_register import auth_register
from .database import clear_data
from .access_error import *


def test_user_profile_sethandle():
    clear_data()
    user1 = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "Bob", "John")

    # this test should pass with no issue
    assert user_profile_sethandle(user1["token"], "handle") == None

    # return a ValueError if the handle is too long
    pytest.raises(ValueError, user_profile_sethandle, user1["token"], "abcdefghijklmnopqrstuvwxyz")

    # if the handle (tested by "handle1") is already in use
    pytest.raises(ValueError, user_profile_sethandle, user2["token"], "handle")
