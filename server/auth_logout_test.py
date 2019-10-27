import pytest
from .auth_logout import auth_logout
from .auth_register import auth_register
from .auth_login import auth_login
from .database import clear_data
from .access_error import *

def test_auth_logout():
    clear_data()
    # following test should fail as user is not logged in!
    dictreg = auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    tokenreg = dictreg["token"]
    auth_logout(tokenreg)   # logging out.
    pytest.raises(ValueError, auth_logout, tokenreg) # trying to logout something already logged out.

    # validtoken test should pass
    dictreg = auth_register("arpitrulania@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = dictreg["token"]
    assert(auth_logout(tokenlog)['is_success']) == True

    # invalid token test should fail
    dictreg = auth_register("arpitinit@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = "invalid"
    pytest.raises(ValueError, auth_logout, tokenlog)
