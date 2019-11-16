# pylint: disable=C0114
# pylint: disable=C0116
# pylint: disable=W0611


import pytest
from .user import (user_profile_setemail, user_profile_sethandle,
                   user_profile_setname, user_profile,
                   user_profiles_uploadphoto, users_all)
from .auth import auth_register
from .database import clear_data, get_user
from .access_error import Value_Error
from .decorators import setup_data


#######################################################################
###  USER_PROFILE_SETEMAIL TESTS HERE #################################
#######################################################################

@setup_data(user_num=2)
def test_user_profile_setemail(users, channels):
    # this test should pass with no issue
    assert user_profile_setemail(users[0]["token"], "z1234567@cse.unsw.edu.au") == {}

    # if the email doesnt exist or is invalid
    pytest.raises(Value_Error, user_profile_setemail, users[0]["token"], "thisisjustastring")

    # if the email is used by another user (check the site)
    pytest.raises(Value_Error, user_profile_setemail, users[1]["token"], "z1234567@cse.unsw.edu.au")


#######################################################################
###  USER_PROFILE_SETHANDLE TESTS HERE ################################
#######################################################################

@setup_data(user_num=2)
def test_user_profile_sethandle(users, channels):
    # this test should pass with no issue
    assert user_profile_sethandle(users[0]["token"], "handle") == {}

    # return a Value_Error if the handle is too long
    pytest.raises(Value_Error, user_profile_sethandle, users[0]["token"], "abcdefghijklmnopqrstuvwxyz")

    # if the handle (tested by "handle1") is already in use
    pytest.raises(Value_Error, user_profile_sethandle, users[1]["token"], "handle")


#######################################################################
###  USER_PROFILE_SETNAME TESTS HERE ##################################
#######################################################################

@setup_data(user_num=1)
def test_user_profile_setname(users, channels):
    # this test should pass with no issue
    assert user_profile_setname(users[0]["token"], "Jane", "Smith") == {}

    # trying to input a first name longer than 50 characters
    pytest.raises(Value_Error, user_profile_setname, users[0]["token"],
                  "a" * 51, "Smith")

    # trying to input a last name longer than 50 characters
    pytest.raises(Value_Error, user_profile_setname, users[0]["token"],
                  "Jane", "a" * 51)

    # assuming we allow mononymous names, at least one value needs to be filled
    assert user_profile_setname(users[0]["token"], "Plato", "") == {}

    # trying to input an empty name
    pytest.raises(Value_Error, user_profile_setname, users[0]["token"], "", "")


#######################################################################
###  USER_PROFILE TESTS HERE ##########################################
#######################################################################

def verify_info1(user_obj, correct_data):
    clear_data()
    # print(message_obj.__dict__)
    if user_obj.__dict__ == correct_data:
        return True
    return False

@setup_data(user_num=1)
def test_user_profile1(users, channels):
    # try to create a valid message
    profile = user_profile(users[0]["token"], 1)

    # check that the database was correctly updated
    assert profile == {
        'u_id': 1,
        'email': "user1@valid.com",
        'name_first': "user1",
        'name_last': "last1",
        'handle_str': "user1last1",
        'profile_img_url': 'static/profile_images/default.jpg'
        }


#######################################################################
###  USER_PROFILE_UPLOAD_PHOTO TESTS HERE #############################
#######################################################################

@setup_data(user_num=1)
def test_user_profiles_uploadphoto(users, channels):
    sample = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/16x16%2BR.jpg/256px-16x16%2BR.jpg"

    # checking for invalid URL
    pytest.raises(ValueError, user_profiles_uploadphoto, users[0]["token"],
                  "cseunsw.edu.au", 0, 0, 199, 199)

    # checking if coordinates are valid
    pytest.raises(Value_Error, user_profiles_uploadphoto, users[0]["token"],
                  sample, -1, -1, 200, 200)

    # checking if cropping area is too big for the image
    pytest.raises(Value_Error, user_profiles_uploadphoto, users[0]["token"],
                  sample, 0, 0, 300, 300)

    # checking sequentialism
    pytest.raises(Value_Error, user_profiles_uploadphoto, users[0]["token"],
                  sample, 20, 20, 10, 10)

    # checking if selection is a square
    pytest.raises(Value_Error, user_profiles_uploadphoto, users[0]["token"],
                  sample, 0, 0, 199, 179)

    pytest.raises(Value_Error, user_profiles_uploadphoto, users[0]["token"],
                  sample, 50, 0, 199, 199)

    # this test should pass with no issue
    assert user_profiles_uploadphoto(users[0]["token"], sample, 0, 0, 199, 199) == {}

#######################################################################
###  USERS_ALL TESTS HERE #############################################
#######################################################################

@setup_data(user_num=3)
def test_users_all(users, channels):
    # testing good functionality (all users should have access):
    assert users_all(users[0]['token']) == {'users': [
            {'u_id': 1,
             'email': 'user1@valid.com',
             'name_first': 'user1',
             'name_last': 'last1',
             'handle_str': 'user1last1',
             'profile_img_url': 'static/profile_images/default.jpg'},
            {'u_id': 2,
             'email': 'user2@valid.com',
             'name_first': 'user2',
             'name_last': 'last2',
             'handle_str': 'user2last2',
             'profile_img_url': 'static/profile_images/default.jpg'},
            {'u_id': 3,
             'email': 'user3@valid.com',
             'name_first': 'user3',
             'name_last': 'last3',
             'handle_str': 'user3last3',
             'profile_img_url': 'static/profile_images/default.jpg'}
        ]}
    
    assert users_all(users[1]['token']) == {'users': [
            {'u_id': 1,
             'email': 'user1@valid.com',
             'name_first': 'user1',
             'name_last': 'last1',
             'handle_str': 'user1last1',
             'profile_img_url': 'static/profile_images/default.jpg'},
            {'u_id': 2,
             'email': 'user2@valid.com',
             'name_first': 'user2',
             'name_last': 'last2',
             'handle_str': 'user2last2',
             'profile_img_url': 'static/profile_images/default.jpg'},
            {'u_id': 3,
             'email': 'user3@valid.com',
             'name_first': 'user3',
             'name_last': 'last3',
             'handle_str': 'user3last3',
             'profile_img_url': 'static/profile_images/default.jpg'}
        ]}
    
    assert users_all(users[2]['token']) == {'users': [
            {'u_id': 1,
             'email': 'user1@valid.com',
             'name_first': 'user1',
             'name_last': 'last1',
             'handle_str': 'user1last1',
             'profile_img_url': 'static/profile_images/default.jpg'},
            {'u_id': 2,
             'email': 'user2@valid.com',
             'name_first': 'user2',
             'name_last': 'last2',
             'handle_str': 'user2last2',
             'profile_img_url': 'static/profile_images/default.jpg'},
            {'u_id': 3,
             'email': 'user3@valid.com',
             'name_first': 'user3',
             'name_last': 'last3',
             'handle_str': 'user3last3',
             'profile_img_url': 'static/profile_images/default.jpg'}
        ]}
    
    # invalid token test:
    pytest.raises(Value_Error, users_all, 'fjngnbfdk')
