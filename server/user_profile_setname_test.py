import pytest
from user_profile_setname import user_profile_setname
from auth_register import auth_register

token = "hewwo"

def test_user_profile_setname():
    user = auth_register("valid@email.com", "12345", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_setname.user_profile_setname(user[token], "Jane", "Smith") == void

    # trying to input a first name longer than 50 characters
    pytest.raises(ValueError, user_profile_setname.user_profile_setname, user[token], "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "Smith")

    # trying to input a last name longer than 50 characters
    pytest.raises(ValueError, user_profile_setname.user_profile_setname, token, "Jane", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")

    # assuming we allow mononymous names, at least one value needs to be filled (first name)
    assert user_profile_setname.user_profile_setname(user[token], "Plato", "") == void

    # trying to input an empty name
    pytest.raises(ValueError, user_profile_setname.user_profile_setname, token, "", "")
