import pytest
from .database import *import pytest
from .database import *
from .auth_register import auth_register
from .channels_create import channels_create
from .message_react import message_react

def verify_message(message_obj, correct_data):
    # print(message_obj.__dict__)
    if message_obj.__dict__ == correct_data:
        return True
    return False

def test_message_react():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }


    # channel_id = channels_create("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI", "channel1", True)
    channel_id = 1
    # db = get_data()

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id, "Hello")

    # check that the message exists
    assert message_1 is not None

    react_id = 1
    message_react(user1["token"], message_1, react_id)
    # check that the database was correctly updated
    assert verify_message(db["message"][0], 
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
                        

def test_no_message():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }

    react_id = 1

    # db = get_data()

    # message is not existed
    assert message_1 is None
    # the message is not existed
    pytest.raises(ValueError, message_react, user1["token"], message_1, react_id)

# def test_message_react():
#     #assert message_react(token, message_id, react_id) == None
#     assert message_react('person2', 3, 1) == None
#     assert message_react('person2', 4, 2) == None
#     assert message_react('person3', 3, 3) == None
#     assert message_react('admin2', 4, 4) == None

#     # Poster reacts on their own message
#     assert message_react('person1', 1, 1) == None
#     assert message_react('admin1', 1, 4) == None

#     with pytest.raises(ValueError, r"*"):
#     #  message_id is not a valid message within a channel that the authorised user has joined
#         message_react('person1', 45, 1)
#         message_react('admin2', 78, 1)
#         message_react('owner', 16, 3)

#     #  react_id is not a valid react ID
#         message_react('person1', 5, 47)
#         message_react('person2', 4, 46) 

#     #  Message with ID message_id already contains an active React with ID react_id
#         message_react('owner',1, 4)
#         message_react('person3', 2, 1)
