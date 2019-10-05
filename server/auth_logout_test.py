import pytest
import auth_logout
import auth_register
import auth_login


def test_validtoken1():
    # following test should fail as user is not logged in!
    dictreg = auth_register.auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    tokenreg = dictreg["token"]
    auth_logout.auth_logout(tokenreg)
    pytest.raises(ValueError, auth_logout.auth_logout, tokenreg)

# validtoken test should pass
def test_validtoken(tokenlog):
    dictreg = auth_register.auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = dictreg["token"]
    assert(auth_logout.auth_logout(tokenlog)) #assuming a successful logout returns a true boolean

# invalid token test should fail
def test_invalidtoken(tokenlog):
    dictreg = auth_register.auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = "invalid"
    pytest.raises(ValueError, auth_logout.auth_logout, tokenlog)

