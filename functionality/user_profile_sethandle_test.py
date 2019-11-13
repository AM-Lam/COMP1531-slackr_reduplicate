import pytest
from .user import user_profile_sethandle
from .auth import auth_register
from .database import clear_data
from .access_error import AccessError, Value_Error


def test_user_profile_sethandle():
    clear_data()
    user1 = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "Bob", "John")

    # this test should pass with no issue
    assert user_profile_sethandle(user1["token"], "handle") == {}

    # return a Value_Error if the handle is too long
    pytest.raises(Value_Error, user_profile_sethandle, user1["token"], "abcdefghijklmnopqrstuvwxyz")

    # if the handle (tested by "handle1") is already in use
    pytest.raises(Value_Error, user_profile_sethandle, user2["token"], "handle")