import pytest
import jwt
from .database import *
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove
from .message_react import message_react
from .message_unreact import message_unreact


def verify_message(message_obj, correct_data):
    # print(message_obj.__dict__)
    if message_obj.__dict__ == correct_data:
        return True
    return False

def test_message_unreact():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }

    channel1 = channels_create(user1["token"], "Channel 1", True)

    channel_id = 1
    db = get_data()

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id, "Hello")

    # check that the message exists
    assert message_1 is not None

    react_id = 1
    message_react(user1["token"], message_1, react_id)
    # check that the database was correctly updated
    assert verify_channel(db["message"][0], 
                        {
                        "message_id" : 1,
                        "u_id" : 111,
                        "text" : "Hello",
                        "channel_id" : 1,
                        "time_sent" : None, 
                        "reacts": [{'u_id': u_id, 'react_id': react_id, 'is_this_user_reacted': True}],
                        "is_pinned": False,
                        }
                        )
                        
    message_unreact(user1["token"], message_1, react_id)
    # check that the database was correctly updated
    assert verify_message(db["message"][0], 
                        {
                        "message_id" : 1,
                        "u_id" : 111,
                        "text" : "Hello",
                        "channel_id" : 1,
                        "time_sent" : None, 
                        "reacts": [],
                        "is_pinned": False,
                        }
                        )

def test_no_message():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }

    db = get_data()
    channel1 = channels_create(user1["token"], "Channel 1", True)

    message_1 = message_send(user1["token"], channel_id, "Hello")
    message_remove(user1["token"], message_1)

    react_id = 1
    
    # message is not existed
    assert message_1 is None
    # the message is not existed
    pytest.raises(ValueError, message_unreact, user1["token"], message_1, react_id)


# def test_message_unreact():
#     # assert message_unreact(token, message_id, react_id) == None
#     assert message_unreact('person1',1,2) == None
#     assert message_unreact('person1',1,2) == None

#     def test_basic_case():
#         message_react('admin2', 4, 4)
#         assert message_unreact('admin2', 4 , 4) == None

#     with pytest.raises(ValueError): 
#     #  message_id is not a valid message within a channel that the authorised user has joined
#         message_unreact('person1', 88, 1)
#         message_unreact('person3', 45, 1)
#         message_unreact('admin1', 78, 1)

#     #  react_id is not a valid React ID
#         message_unreact('person3', 3, 18)
#         message_unreact('admin2', 3, 28) 

#     #  Message with ID message_id already contains an active React with ID react_id
#     def test_double_unreact():
#         message_react('person2', 3, 3)
#         message_unreact('person1', 1, 3)
#         with pytest.raises(ValueError):
#             message_unreact('person1', 1, 3)
