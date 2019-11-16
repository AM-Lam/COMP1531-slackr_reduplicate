# pylint: disable=C0114
# pylint: disable=C0116
# pylint: disable=W0611


import pytest
from .user import (user_profile_setemail, user_profile_sethandle,
                   user_profile_setname, user_profile,
                   user_profiles_uploadphoto)
from .auth import auth_register
from .database import clear_data
from .access_error import Value_Error


#######################################################################
###  USER_PROFILE_SETEMAIL TESTS HERE #################################
#######################################################################

def test_user_profile_setemail():
    clear_data()
    user1 = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "John", "Zed")

    # this test should pass with no issue
    assert user_profile_setemail(user1["token"], "z1234567@cse.unsw.edu.au") == {}

    # if the email doesnt exist or is invalid
    pytest.raises(Value_Error, user_profile_setemail, user1["token"], "thisisjustastring")

    # if the email is used by another user (check the site)
    pytest.raises(Value_Error, user_profile_setemail, user2["token"], "z1234567@cse.unsw.edu.au")


#######################################################################
###  USER_PROFILE_SETHANDLE TESTS HERE ################################
#######################################################################

def test_user_profile_sethandle():
    clear_data()
    user1 = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "Bob", "John")

    # this test should pass with no issue
    assert user_profile_sethandle(user1["token"], "handle") == {}

    # return a Value_Error if the handle is too long
    pytest.raises(Value_Error, user_profile_sethandle, user1["token"], "abcdefghijklmnopqrstuvwxyz")

    # if the handle (tested by "handle1") is already in use
    pytest.raises(Value_Error, user_profile_sethandle, user2["token"], "handle")


#######################################################################
###  USER_PROFILE_SETNAME TESTS HERE ##################################
#######################################################################

def test_user_profile_setname():
    clear_data()
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # this test should pass with no issue
    assert user_profile_setname(user["token"], "Jane", "Smith") == {}

    # trying to input a first name longer than 50 characters
    pytest.raises(Value_Error, user_profile_setname, user["token"],
                  "a" * 51, "Smith")

    # trying to input a last name longer than 50 characters
    pytest.raises(Value_Error, user_profile_setname, user["token"],
                  "Jane", "a" * 51)

    # assuming we allow mononymous names, at least one value needs to be filled
    assert user_profile_setname(user["token"], "Plato", "") == {}

    # trying to input an empty name
    pytest.raises(Value_Error, user_profile_setname, user["token"], "", "")


#######################################################################
###  USER_PROFILE TESTS HERE ##########################################
#######################################################################

def verify_info1(user_obj, correct_data):
    clear_data()
    # print(message_obj.__dict__)
    if user_obj.__dict__ == correct_data:
        return True
    return False

def test_user_profile1():
    clear_data()
    user1 = auth_register("valid@email.com", "1234567", "Bob", "Jones")

    # try to create a valid message
    profile = user_profile(user1["token"], 1)

    # check that the user exists
    assert profile is not None

    # check that the database was correctly updated
    assert profile == {
        'email': "valid@email.com",
        'name_first': "Bob",
        'name_last': "Jones",
        'handle_str': "BobJones"
        }


#######################################################################
###  USER_PROFILE_UPLOAD_PHOTO TESTS HERE #############################
#######################################################################

def test_user_profiles_uploadphoto():
    clear_data()

    user = auth_register("valid@email.com", "1234567890", "John", "Doe")
    assert user is not None

    # tests will go here in iteration 3


############################################################################################################################
###  USER_PROFILE_UPLOAD_PHOTO TESTS HERE ##################################################################################
############################################################################################################################

def test_users_all():
    clear_data()
    user1 = auth_register("valid@email.com", "1234567", "Bob", "Jones")
    user2 = auth_register("valid1@email.com", "11221122", "Sally", "Salmon")

    user_t = get_user(user1['u_id'])
    user_u = get_user(user2['u_id'])
    # testing good functionality:
    assert users_all(user1['token']) == {'users':['BobJones','SallySalmon']}
    # invalid token test:
    pytest.raises(Value_Error, users_all, 'fjngnbfdk')
    

