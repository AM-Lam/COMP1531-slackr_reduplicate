import pytest
import hashlib
from .auth_register import auth_register
from .auth_passwordreset_request import auth_passwordreset_request
from .auth_passwordreset_reset import auth_passwordreset_reset, chec_password_strength
from .database import clear_data, get_data
from .access_error import *


def test_reset_test():
    clear_data()
    auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    auth_passwordreset_request('user1@gmail.com')

    # write more tests to check code
    pytest.raises(ValueError, auth_passwordreset_reset, "INVALID-CODE" , 'abcdefgh')

    pytest.raises(ValueError, auth_passwordreset_reset, "123@!@" , 'abcdefgh')

    assert chec_password_strength("sdfadffsfsfeasdadew")

    pytest.raises(ValueError, chec_password_strength, 'pew')

    ###########################################################################

    # now lets send a reset request
    reset_code = auth_passwordreset_request('user1@gmail.com')
    # now reset the password
    auth_passwordreset_reset(reset_code, 'abcdefgh')
    hashed_pass = (hashlib.sha256('abcdefgh'.encode()).hexdigest())
    flag = 0
    update_data = get_data()
    for i in update_data['users']:
        if i._email == 'user1@gmail.com':
            if i._password == hashed_pass:
                flag = 1
    assert flag == 1
