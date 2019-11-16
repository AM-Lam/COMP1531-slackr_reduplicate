# pylint: disable=C0114
# pylint: disable=C0116


import hashlib
import pytest
from .database import clear_data, get_data, get_user
from .auth import (auth_login, auth_register, auth_logout,
                   auth_passwordreset_request, auth_passwordreset_reset,
                   admin_userpermission_change)
from .access_error import AccessError, Value_Error
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
    pytest.raises(Value_Error, auth_register, 'user1@valid.com', 'passew@321',
                  'user', 'a')


@setup_data()
def test_register3(users, channels):
    # raise an error if user tries to register with a very long name
    #-> first name too long
    pytest.raises(Value_Error, auth_register, 'user5@valid.com',
                  'passew@321', 'x' * 100, 'o')
    #-> last name too long
    pytest.raises(Value_Error, auth_register, 'user6@valid.com',
                  'passew@321', 'o', 'x' * 100)


@setup_data()
def test_register4(users, channels):
    # raise error if password is weak!
    pytest.raises(Value_Error, auth_register, 'user7@valid.com', 'pew', 'user',
                  'a')


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


@setup_data(user_num=2)
def test_reset_reset1(users, channels):
    # raise errors if the reset code is incorrect, use the 2nd user to
    # test that the email is sent to the correct user if there is more
    # than one character
    code = auth_passwordreset_request('user2@valid.com')

    # invalid codes being passed in!
    pytest.raises(Value_Error, auth_passwordreset_reset, "INVALID-CODE",
                  'abcdefgh')

    # password not strong
    pytest.raises(Value_Error, auth_passwordreset_reset, code, 'ab')

    # remove the user from the database then attempt to reset their data
    get_data()["users"].pop(users[1]["u_id"])

    pytest.raises(Value_Error, auth_passwordreset_reset, code, '222222')


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


@setup_data(user_num=4)
def test_admin_userpermission_change(users, channels):
    # as a slackr owner attempt to make a member an admin
    assert admin_userpermission_change(users[0]["token"],
                                       users[1]["u_id"], 2) == {}

    # as an admin attempt to make a member an admin
    assert admin_userpermission_change(users[1]["token"],
                                       users[2]["u_id"], 2) == {}

    # as an admin try to make a slackr owner a member, this should fail
    pytest.raises(AccessError, admin_userpermission_change, users[1]["token"],
                  users[0]["u_id"], 3)

    # as an admin try to make an admin a slackr owner, this should fail
    pytest.raises(AccessError, admin_userpermission_change, users[1]["token"],
                  users[2]["u_id"], 1)

    # as a regular member try to change somebody's perms, this should fail
    pytest.raises(AccessError, admin_userpermission_change, users[3]["token"],
                  users[2]["u_id"], 3)

    # try to run with an invalid token
    pytest.raises(Value_Error, admin_userpermission_change, 000,
                  users[2]["u_id"], 1)

    # try to change the permissions of a user that does not exist
    pytest.raises(Value_Error, admin_userpermission_change, users[1]["token"],
                  666, 3)

    # try to change to a permision_id that is invalid (too low), this should
    # fail
    pytest.raises(Value_Error, admin_userpermission_change, users[1]["token"],
                  users[3]["u_id"], 0)

    # try to change to a permision_id that is invalid (too high), this should
    # fail
    pytest.raises(Value_Error, admin_userpermission_change, users[1]["token"],
                  users[3]["u_id"], 4)
