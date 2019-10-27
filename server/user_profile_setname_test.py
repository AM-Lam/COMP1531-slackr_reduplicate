import pytest
from .user_profile_setname import user_profile_setname
from .auth_register import auth_register
from .database import clear_data
from .access_error import *


def test_user_profile_setname():
    clear_data()
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_setname(user["token"], "Jane", "Smith") == None

    # trying to input a first name longer than 50 characters
    pytest.raises(ValueError, user_profile_setname, user["token"],
                  "a" * 51, "Smith")

    # trying to input a last name longer than 50 characters
    pytest.raises(ValueError, user_profile_setname, user["token"],
                 "Jane", "a" * 51)

    # assuming we allow mononymous names, at least one value needs to be filled
    assert user_profile_setname(user["token"], "Plato", "") == None

    # trying to input an empty name
    pytest.raises(ValueError, user_profile_setname, user["token"], "", "")
