import auth_register
import auth_login
import auth_passwordreset_request
import auth_passwordreset_reset
import pytest


auth_register.auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
auth_passwordreset_request('user1@gmail.com')

def test_check_reset_code():
    # write more tests to check code
    pytest.raises(ValueError, auth_passwordreset_reset.auth_passwordreset_reset, "INVALID-CODE")

def test_code_is_not_string():
    pytest.raises(ValueError, auth_passwordreset_reset.auth_passwordreset_reset, 123@!@)

#########################################################################################

def test_password_strength0():
    assert(auth_passwordreset_reset.chec_password_strength("sdfadffsfsfeasdadew"))

def test_password_strength01():
    pytest.raises(ValueError, auth_passwordreset_reset.chec_password_strength, 'pew')