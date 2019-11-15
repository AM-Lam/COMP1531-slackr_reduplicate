# pylint: disable=C0114
# pylint: disable=C0116


import hashlib
import pytest
from .database import clear_data, get_data, get_user
from .auth import (auth_login, auth_register, auth_logout,
                   auth_passwordreset_request, auth_passwordreset_reset)
from .access_error import Value_Error
from .decorators import setup_data


###############################################################################
###  LOGOUT TESTS HERE ########################################################
###############################################################################


@setup_data(user_num=1)
def test_auth_logout1(users, channels):
    # following test should fail as user is not logged in!
    tokenreg = users[0]["token"]

    # logging out.
    auth_logout(tokenreg)

    # trying to logout something already logged out.
    pytest.raises(Value_Error, auth_logout, tokenreg)


@setup_data(user_num=1)
def test_auth_logout2(users, channels):
    # validtoken test should pass
    tokenlog = users[0]["token"]
    assert(auth_logout(tokenlog)['is_success']) == True


@setup_data()
def test_auth_logout3(users, channels):
    # pylint: disable=W0612

    # invalid token test should fail
    tokenlog = "invalid"
    pytest.raises(Value_Error, auth_logout, tokenlog)


###############################################################################
###  LOGIN TESTS HERE #########################################################
###############################################################################

@setup_data(user_num=1)
def test_login1(users, channels):
    # simple test to make sure login works overall
    # what if the email and password combo is valid? -->
    dictio = auth_login('user1@valid.com', '111111')
    assert dictio['token'] is not None
    assert dictio['u_id'] is not None

@setup_data(user_num=1)
def test_login2(users, channels):
    # test should fail if user tries to login with wrong email
    # here we assume that an existing database has logged the
    # information of user1 and user2 created above
    # what if the email does not exist in the database -->
    pytest.raises(Value_Error, auth_login, 'INVALIDeMAIL@valid.com', '111111')   

    # user forgot to put the .au domain in the address-->
    pytest.raises(Value_Error, auth_login, 'user3@valid.com.au', '111111')


@setup_data(user_num=2)
def test_login3(users, channels):
    # test should fail if password is wrong or not of correct length!
    # what if the password does not have Enough characters? -->
    pytest.raises(Value_Error, auth_login, 'user1@valid.com', 'pas31')

    # what if the password field was just left empty> -->
    pytest.raises(Value_Error, auth_login, 'user1@valid.com', '')

    # what is password has a valid length but is incorrect? -->
    pytest.raises(Value_Error, auth_login, 'user1@valid.com' , '222222')

    # what if the password exists on the server but is not correctly
    # matched to the provided email -->
    pytest.raises(Value_Error, auth_login, 'user2@valid.com.au' , '111111')


###############################################################################
###  REGISTER TESTS HERE ######################################################
###############################################################################


@setup_data(user_num=1)
def test_register1(users, channels):
    # simple test to make sure register works overall
    assert users[0]['token'] is not None
    assert users[0]['u_id'] is not None


@setup_data(user_num=1)
def test_register2(users, channels):
    # raise error if user tries to register more than once
    assert users[0]['token'] is not None
    assert users[0]['u_id'] is not None
    pytest.raises(Value_Error, auth_register, 'user1@valid.com', 'passew@321', 'user', 'a')


@setup_data()
def test_register3(users, channels):
    # raise an error if user tries to register with a very long name
    #-> first name too long
    pytest.raises(Value_Error, auth_register, 'user5@valid.com', 'passew@321', 'userdhksfbskhdbfkhsdbvhkfsbvhfbvhkdbfvhkbdfkhbvhkdfbvkhdfbvhkdfbvhkdfbvkhdbfvhkbdfkhbvdfhkb', 'o')
    #-> last name too long
    pytest.raises(Value_Error, auth_register, 'user6@valid.com', 'passew@321', 'o', 'userdhksfbskhdbfkhsdbvhkfsbvhfbvhkdbfvhkbdfkhbvhkdfbvkhdfbvhkdfbvhkdfbvkhdbfvhkbdfkhbvdfhkb')


@setup_data()
def test_register4(users, channels):
    # raise error if password is weak!
    pytest.raises(Value_Error, auth_register, 'user7@valid.com', 'pew', 'user', 'a')


###############################################################################
### PASSWORD RESET REQUEST TESTS HERE #########################################
###############################################################################


@setup_data(user_num=1)
def test_reset_request(users, channels):
    # testing if the code is generated and stored successfully!
    # can't test email send since send email send code has been moved
    # to server.py i.e. flask.

    update_data = get_data()
    reset_code = auth_passwordreset_request('user1@valid.com')
    assert(update_data["reset"][reset_code]) == 'user1@valid.com'


###############################################################################
### PASSWORD RESET RESET TESTS HERE ###########################################
###############################################################################

@setup_data(user_num=1)
def test_reset_reset1(users, channels):
    # raise errors if the reset code is incorrect.
    auth_passwordreset_request('user1@valid.com')
    #-> invalid codes being passed in!
    pytest.raises(Value_Error, auth_passwordreset_reset, "INVALID-CODE",
                  'abcdefgh')
    #->password not strong
    pytest.raises(Value_Error, auth_passwordreset_reset, "123@!@", 'ab')

@setup_data(user_num=1)
def test_reset_reset2(users, channels):
    # testing is it works!
    # now lets send a reset request.
    reset_code = auth_passwordreset_request('user1@valid.com')
    # now reset the password.
    auth_passwordreset_reset(reset_code, 'abcdefgh')
    hashed_pass = (hashlib.sha256('abcdefgh'.encode()).hexdigest())

    all_users = get_data()["users"]
    for u_id in all_users:
        user = get_user(u_id)
        if user.get_email() == 'user1@valid.com':
            assert user.get_password() == hashed_pass
            break
