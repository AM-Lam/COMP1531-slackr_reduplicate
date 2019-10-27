from .auth_register import *
from .auth_passwordreset_request import *
from .auth_passwordreset_reset import *
from .database import *
import pytest


def test_reset_test():
    clear_data()
    auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    auth_passwordreset_request('user1@gmail.com')

    # write more tests to check code
    pytest.raises(ValueError, auth_passwordreset_reset, "INVALID-CODE")

    pytest.raises(ValueError, auth_passwordreset_reset, "123@!@")

    assert(chec_password_strength("sdfadffsfsfeasdadew"))

    pytest.raises(ValueError, chec_password_strength, 'pew')
