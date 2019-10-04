from user_profiles_uploadphoto import user_profiles_uploadphoto
from auth_register import register
import pytest

def test_user_profiles_uploadphoto():
    user = register("valid@email.com", "12345", "John", "Doe")

    # this test should pass with no issue
    assert user_profiles_uploadphoto(user["token"], "https://twitter.com/home", 0, 0, 200, 200) == None

    # checking for invalid URL
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "notarealurl", 0, 0, 200, 200)

    # checking if coordinates are valid
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "https://twitter.com/home", -1, -1, 200, 200)
