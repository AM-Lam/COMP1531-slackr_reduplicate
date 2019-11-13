import pytest
from .user import user_profiles_uploadphoto
from .auth import auth_register
from .database import clear_data
from .access_error import AccessError, Value_Error


def test_user_profiles_uploadphoto():
    clear_data()
    
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")
    assert user is not None

    # tests will go here in iteration 3
