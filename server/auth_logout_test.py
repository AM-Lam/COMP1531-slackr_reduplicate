import pytest
from .auth_logout import *
from .auth_register import *
from .auth_login import *


def test_validtoken1():
    # following test should fail as user is not logged in!
    dictreg = auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    tokenreg = dictreg["token"]
    auth_logout(tokenreg)   # logging out.
    pytest.raises(ValueError, auth_logout, tokenreg) # trying to logout something already logged out.

# validtoken test should pass
def test_validtoken():
    dictreg = auth_register("arpitrulania@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = dictreg["token"]
    assert(auth_logout(tokenlog)['is_success']) == True #assuming a successful logout returns a true boolean

# invalid token test should fail
def test_invalidtoken():
    dictreg = auth_register("arpitinit@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = "invalid"    # <-user tries to fool the system by passing any random token.
    pytest.raises(ValueError, auth_logout, tokenlog)

