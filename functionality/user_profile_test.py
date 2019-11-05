import pytest
from .access_error import AccessError, ValueError
from .auth import auth_register
from .user import user_profile
from .database import clear_data

def verify_info(user_obj, correct_data):
    clear_data()
    # print(message_obj.__dict__)
    if user_obj.__dict__ == correct_data:
        return True
    return False

def test_user_profile():
    clear_data()
    user1 = auth_register("valid@email.com", "1234567", "Bob", "Jones")

    # try to create a valid message
    profile = user_profile(user1["token"], 1)

    # check that the user exists
    assert profile is not None

    # check that the database was correctly updated
    assert profile == {'email': "valid@email.com", 'name_first': "Bob", 'name_last': "Jones", 'handle_str': "BobJones"}
