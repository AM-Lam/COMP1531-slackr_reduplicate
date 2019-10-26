from .user_profiles_uploadphoto import user_profiles_uploadphoto
from .auth_register import auth_register
from .access_error import AccessError
import pytest

def test_user_profiles_uploadphoto():
    user = auth_register("valid@email.com", "123456", "John", "Doe")

    # this test should pass with no issue
    assert user_profiles_uploadphoto(user["token"], "https://twitter.com/home", 0, 0, 200, 200) == None

    # checking for invalid URL
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "notarealurl", 0, 0, 200, 200)

    # checking if coordinates are valid
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "https://twitter.com/home", -1, -1, 200, 200)
    # here having an image size of 300 may be valid, for now the max for testing is 200 though
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "https://twitter.com/home", -1, -1, 300, 300)

    # checking sequentialism
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "https://twitter.com/home", 20, 20, 10, 200)

    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "https://twitter.com/home", 20, 20, 200, 10)

    # checking if selection is a square
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "https://twitter.com/home", 0, 0, 200, 180)

    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "https://twitter.com/home", 50, 0, 200, 200)
