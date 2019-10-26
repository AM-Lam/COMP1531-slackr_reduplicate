from .auth_register import *
from .auth_passwordreset_request import *
from .auth_passwordreset_reset import *
from .database import *
import pytest


clear_data()
auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
auth_passwordreset_request('user1@gmail.com')


def test_check_reset_code():
    # write more tests to check code
    pytest.raises(ValueError, auth_passwordreset_reset, "INVALID-CODE")

def test_code_is_not_string():
    pytest.raises(ValueError, auth_passwordreset_reset, "123@!@")

#########################################################################################

def test_password_strength0():
    assert(chec_password_strength("sdfadffsfsfeasdadew"))

def test_password_strength01():
    pytest.raises(ValueError, chec_password_strength, 'pew')
