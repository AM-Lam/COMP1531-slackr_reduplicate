import pytest
import hashlib
import re
from .database import clear_data, get_data, get_user
from .auth import (auth_login, auth_register, auth_logout,
                   auth_passwordreset_request, auth_passwordreset_reset)
from .access_error import AccessError, Value_Error


############################################################################################################################
###  LOGOUT TESTS HERE #####################################################################################################
############################################################################################################################

def test_auth_logout1():
    clear_data()
    # following test should fail as user is not logged in!
    dictreg = auth_register("arpit@gmail.com", "passwording", "arpit", "rulania")
    tokenreg = dictreg["token"]
    auth_logout(tokenreg)   # logging out.
    pytest.raises(Value_Error, auth_logout, tokenreg) # trying to logout something already logged out.

def test_auth_logout2():
    # validtoken test should pass
    clear_data()
    dictreg = auth_register("arpitrulania@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = dictreg["token"]
    assert(auth_logout(tokenlog)['is_success']) == True

def test_auth_logout3():
    # invalid token test should fail
    clear_data()
    dictreg = auth_register("arpitinit@gmail.com", "passwording", "arpit", "rulania")
    tokenlog = "invalid"
    pytest.raises(Value_Error, auth_logout, tokenlog)


############################################################################################################################
###  LOGIN TESTS HERE ######################################################################################################
############################################################################################################################


def test_login1():
    # simple test to make sure login works overall
    clear_data()
    user_1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user_2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
    user_3 = auth_register('user3@domain.com.au' , 'vsdco23111' , 'person' , 'c')

    assert user_1 is not None
    assert user_2 is not None
    assert user_3 is not None
    
    # what if the email and password combo is valid? -->
    dictio = auth_login('user1@domain.com' ,'passew@321')
    assert dictio['token'] is not None
    assert dictio['u_id'] is not None

def test_login2():
    # test should fail if user tries to login with wrong email
    clear_data()
    user_1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user_2 = auth_register('user2@student.unsw.edu.au' , 'vscod231343' , 'ussr' , 'b')
    user_3 = auth_register('user3@domain.com.au' , 'vsdco23111' , 'person' , 'c')

    assert user_1 is not None
    assert user_2 is not None
    assert user_3 is not None
    
    # here we assume that an existing database has logged the information of user1 and user2 created above
    # what if the email does not exist in the database -->
    pytest.raises(Value_Error, auth_login, 'INVALIDeMAIL@domain.com', 'abcdefgh')   
    # user forgot to put the .au domain in the address-->
    pytest.raises(Value_Error, auth_login, 'user3@domain.com', 'abcdefgh')
    # did the user forget to put the subdomain (i.e. student.unsw....)? -->
    pytest.raises(Value_Error, auth_login, 'user2@unsw.edu.au', 'abcdefgh')
    # does my function only accept a particular domain? -->
    pytest.raises(Value_Error, auth_login, 'user3@gmail.com.au', 'abcdefgh')

def test_login3():
    # test should fail if password is wrong or not of correct length!
    clear_data()
    user_1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user_2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
    user_3 = auth_register('user3@domain.com.au' , 'vsdco23111' , 'person' , 'c')

    assert user_1 is not None
    assert user_2 is not None
    assert user_3 is not None
    
    # what if the password does not have Enough characters? -->
    pytest.raises(Value_Error, auth_login, 'user1@domain.com' , 'pas31')
    # what if the password field was just left empty> -->
    pytest.raises(Value_Error, auth_login, 'user1@domain.com' , '')
    # what is password has a valid length but is incorrect? -->
    pytest.raises(Value_Error, auth_login, 'user1@domain.com' , 'passwordisthis')
    # what if the password exists on the server but is not correctly matched to the provided email -->
    pytest.raises(Value_Error, auth_login, 'user3@domain.com' , 'passew@321')


############################################################################################################################
###  REGISTER TESTS HERE ###################################################################################################
############################################################################################################################


def test_register1():
    # simple test to make sure register works overall
    clear_data()
    token = auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    assert token['token'] is not None
    assert token['u_id'] is not None

def test_register2():
    # raise error if user tries to register more than once
    clear_data()
    token = auth_register('user1@gmail.com', 'passew@321', 'user', 'one')
    assert token['token'] is not None
    assert token['u_id'] is not None
    pytest.raises(Value_Error, auth_register, 'user1@gmail.com', 'passew@321', 'user', 'one' )

def test_register3():
    # raise an error if user tries to register with a very long name
    clear_data()
    #-> first name too long
    pytest.raises(Value_Error, auth_register, 'user1@gmail.com', 'passew@321', 'userdhksfbskhdbfkhsdbvhkfsbvhfbvhkdbfvhkbdfkhbvhkdfbvkhdfbvhkdfbvhkdfbvkhdbfvhkbdfkhbvdfhkb', 'o')
    #-> last name too long
    pytest.raises(Value_Error, auth_register, 'user1@gmail.com', 'passew@321', 'o', 'userdhksfbskhdbfkhsdbvhkfsbvhfbvhkdbfvhkbdfkhbvhkdfbvkhdfbvhkdfbvhkdfbvkhdbfvhkbdfkhbvdfhkb')

def test_register4():
    # raise error if password is weak!
    clear_data()
    pytest.raises(Value_Error, auth_register, 'user1@gmail.com', 'pew', 'user', 'one' )


############################################################################################################################
### PASSWORD RESET REQUEST TESTS HERE ######################################################################################
############################################################################################################################


def test_reset_request():
    # testing if the code is generated and stored successfully!
    clear_data()
    auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    ## cant test email send since send email send code has been moved to server.py i.e. flask.
    update_data = get_data()
    reset_code = auth_passwordreset_request('user1@domain.com')
    assert(update_data["reset"][reset_code]) == 'user1@domain.com'


############################################################################################################################
### PASSWORD RESET RESET TESTS HERE ########################################################################################
############################################################################################################################


def test_reset_reset1():
    # raise errors if the reset code is incorrect.
    clear_data()
    auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    auth_passwordreset_request('user1@gmail.com')
    #-> invalid codes being passed in!
    pytest.raises(Value_Error, auth_passwordreset_reset, "INVALID-CODE" , 'abcdefgh')
    #->password not strong
    pytest.raises(Value_Error, auth_passwordreset_reset, "123@!@" , 'ab')

def test_reset_reset2():
    # testing is it works!
    clear_data()
    auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    # now lets send a reset request.
    reset_code = auth_passwordreset_request('user1@gmail.com')
    # now reset the password.
    auth_passwordreset_reset(reset_code, 'abcdefgh')
    hashed_pass = (hashlib.sha256('abcdefgh'.encode()).hexdigest())
    
    all_users = get_data()["users"]
    for u_id in all_users:
        user = get_user(u_id)
        if user.get_email() == 'user1@gmail.com':
            assert user.get_password() == hashed_pass
            break

