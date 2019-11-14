import pytest
from .user import user_profile_setemail
from .auth import auth_register
from .database import clear_data
from .access_error import *

def test_user_profile_setemail():
    clear_data()

    user1 = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "John", "Zed")

    # this test should pass with no issue
    assert user_profile_setemail(user1["token"], "z1234567@cse.unsw.edu.au") == {}

    # if the email doesnt exist or is invalid
    pytest.raises(ValueError, user_profile_setemail, user1["token"], "thisisjustastring")

    # if the email is used by another user (check the site)
    pytest.raises(ValueError, user_profile_setemail, user2["token"], "z1234567@cse.unsw.edu.au")
