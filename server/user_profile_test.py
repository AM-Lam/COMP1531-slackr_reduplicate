import pytest
from .access_error import AccessError
from .auth_register import auth_register
from .user_profile import user_profile
from .database import *

def verify_info(user_obj, correct_data):
    # print(message_obj.__dict__)
    if user_obj.__dict__ == correct_data:
        return True
    return False

def test_user_profile():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }

    db = get_data()
    
    # try to create a valid message
    profile = user_profile(user1["token"], 111)

    # check that the user exists
    assert profile is not None

    # check that the database was correctly updated
    assert profile == {'email': "valid@email.com", 'name_first': "Bob", 'name_last': "Jones", 'handle_str': "BobJones"}

# def test_user_profile():
#     # assert user_profile(token, u_id) == [{email, name_first, name_last, handle_str}]
#     assert user_profile('person1', 123) == {'hayden@gmail.com', 'Hayden', 'Smith', 'handle'}
#     assert user_profile('person2', 456) == {'smith@gmail.com', 'Smith', 'Hayden', 'handler'}
#     assert user_profile('person3', 789) == {'person@gmail.com', 'one', 'person', '1st'}
#     assert user_profile('admin1', 11) == {'admin1@gmail.com', 'one', 'admin', 'admin1'}
#     assert user_profile('admin2', 22) == {'admin2@gmail.com', 'two', 'admin', 'admin2'}
#     assert user_profile('owner', 159) =={'owner@gmail.com', 'Owner', 'UNSW', 'handler'}

#     # ValueError: User with u_id is not a valid user
#     with pytest.raises(ValueError):
#         #unmatching token and u_id
#         user_profile('person1', 465)
#         user_profile('person3', 789)
#         user_profile('person1', 22)
#         user_profile('person2', 22)
#         user_profile('admin1', 123)
#         user_profile('admin2', 11)

#         # typo or wrong token
#         user_profile('Person1', 123)
#         user_profile('oner', 159)
#         user_profile('peraon3', 789)
#         user_profile('person', 22)


