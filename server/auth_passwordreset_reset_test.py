from .auth_register import *
from .auth_passwordreset_request import *
from .auth_passwordreset_reset import *
from .database import *
import pytest
import hashlib


auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
auth_passwordreset_request('user1@gmail.com')

def test_check_reset_code():
    # write more tests to check code
    pytest.raises(ValueError, auth_passwordreset_reset, "INVALID-CODE" , 'abcdefgh')

def test_code_is_not_string():
    pytest.raises(ValueError, auth_passwordreset_reset, "123@!@" , 'abcdefgh')

#########################################################################################

def test_password_strength0():
    assert(chec_password_strength("sdfadffsfsfeasdadew"))

def test_password_strength01():
    pytest.raises(ValueError, chec_password_strength, 'pew')

#########################################################################################

def test_working():
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
