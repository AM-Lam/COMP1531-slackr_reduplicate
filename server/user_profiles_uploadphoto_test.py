from user_profiles_uploadphoto import user_profiles_uploadphoto
from auth_register import auth_register
import pytest
token = "hewwo"

def test_user_profiles_uploadphoto():
    user = auth_register("valid@email.com", "12345", "John", "Doe")

    # this test should pass with no issue
    assert user_profiles_uploadphoto.user_profiles_uploadphoto(user[token], "https://twitter.com/home", 0, 0, 200, 200) == void

    # checking for invalid URL
    pytest.raises(ValueError, user_profiles_uploadphoto.user_profiles_uploadphoto, token, "notarealurl", 0, 0, 200, 200)

    # checking if coordinates are valid
    pytest.raises(ValueError, user_profiles_uploadphoto.user_profiles_uploadphoto(user[token], "https://twitter.com/home", -1, -1, 200, 200)
