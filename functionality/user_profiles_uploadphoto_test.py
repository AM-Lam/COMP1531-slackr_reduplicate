import pytest
from .user import user_profiles_uploadphoto
from .auth import auth_register
from .database import clear_data
from .access_error import *

def test_user_profiles_uploadphoto():
    clear_data()

    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # NOTE: for an image with width 200, end co-ordinates must be 199
    sample = "https://upload.wikimedia.org/wikipedia/commons/1/1b/Square_200x200.png"

    # checking for invalid URL
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], "cseunsw.edu.au", 0, 0, 199, 199)

    # checking if coordinates are valid
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], sample, -1, -1, 200, 200)

    # checking if cropping area is too big for the image
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], sample, 0, 0, 300, 300)

    # checking sequentialism
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], sample, 20, 20, 10, 10)

    # checking if selection is a square
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], sample, 0, 0, 199, 179)
    pytest.raises(ValueError, user_profiles_uploadphoto, user["token"], sample, 50, 0, 199, 199)

    # this test should pass with no issue
    assert user_profiles_uploadphoto(user["token"], sample, 0, 0, 199, 199) == {}
