from user_profile_setemail import user_profile_setemail
from auth_register import auth_register
import pytest
token = "hewwo"

def test_user_profile_setemail():
    user = auth_register("valid@email.com", "12345", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_setemail.user_profile_setemail(user[token], "z1234567@cse.unsw.edu.au") == void

    # if the email doesnt exist or is invalid
    pytest.raises(ValueError, user_profile_setemail.user_profile_setemail, user[token], "thisisjustastring")

    # if the email is used by another user (check the site)
    pytest.raises(ValueError, user_profile_setemail.user_profile_setemail, user[token], "cs1531@cse.unsw.edu.au")
