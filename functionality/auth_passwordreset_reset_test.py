import pytest
import hashlib
from .database import clear_data, get_data
from .auth import auth_passwordreset_request, auth_passwordreset_reset, auth_register
from .access_error import AccessError, Value_Error


def test_reset_test():
    clear_data()
    
    auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    auth_passwordreset_request('user1@gmail.com')

    # write more tests to check code
    pytest.raises(Value_Error, auth_passwordreset_reset, "INVALID-CODE" , 'abcdefgh')
    pytest.raises(Value_Error, auth_passwordreset_reset, "123@!@" , 'abcdefgh')

    ###########################################################################

    # now let's send a reset request
    reset_code = auth_passwordreset_request('user1@gmail.com')
    
    # now reset the password
    auth_passwordreset_reset(reset_code, 'abcdefgh')
    hashed_pass = hashlib.sha256('abcdefgh'.encode()).hexdigest()
    flag = 0
    update_data = get_data()
    for i in update_data['users']:
        if i.get_email() == 'user1@gmail.com':
            if i.get_password() == hashed_pass:
                flag = 1
    assert flag == 1
