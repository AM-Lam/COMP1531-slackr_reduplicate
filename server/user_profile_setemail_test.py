import pytest
from .user_profile_setemail import user_profile_setemail
from .auth_register import auth_register
from .access_error import *
from .database import *


clear_data()


def test_user_profile_setemail():
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_setemail(user["token"], "z1234567@cse.unsw.edu.au") == None

    # if the email doesnt exist or is invalid
    pytest.raises(ValueError, user_profile_setemail, user["token"], "thisisjustastring")

    # if the email is used by another user (check the site)
    pytest.raises(ValueError, user_profile_setemail, user["token"], "cs1531@cse.unsw.edu.au")
