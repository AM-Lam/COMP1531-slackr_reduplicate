import pytest
import auth_logout
import auth_register
import auth_login


def test_validtoken1():
    # following test should fail as user is not logged in!
    dictreg = auth_register.auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    tokenreg = dictreg["token"]
    pytest.raises(ValueError, auth_logout.auth_logout, tokenreg)

# validtoken test should pass
def test_validtoken(tokenlog):
    dictreg = auth_register.auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    dictlog = auth_login.auth_login("arpit@gmail.com", "passwording")
    tokenlog = dictlog["token"]
    assert(auth_logout.auth_logout(tokenlog)) #assuming a successful logout returns a true boolean

# invalid token test should fail
def test_invalidtoken(tokenlog):
    dictreg = auth_register.auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    dictlog = auth_login.auth_login("arpit@gmail.com", "passwording")
    tokenlog = dictlog["token"]
    pytest.raises(ValueError, auth_logout.auth_logout, tokenlog)


## assuming auth_register does not login the person