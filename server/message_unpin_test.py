import pytest
from .database import *
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_leave import channel_leave

def test_message_unpin():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }
    user2 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMjIifQ.V8RNVCtIW66E7gxk54-FYE_XRp67TsndcrCmZMfJ0RI"
    }
    user3 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMyJ9.QaiuthhOZ3vU8iRd7QDtbs89nDHpNo6lKgo_JPwpSj4"
    }

    # channel_id = channels_create("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI", "channel1", True)
    channel_id = 1
    db = get_data()

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id, "Hello")

    # check that the channel exists
    assert message_1 is not None
    message_pin(user1["token"], message_1)
    assert db['message'][0]._pinned == True
    message_unpin(user1["token"], message_1)
    assert db['message'][0]._pinned == False

def test_no_message1():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }

    # db = get_data()

    # message is not existed
    assert message_1 is None
    # the message is not existed
    pytest.raises(ValueError, message_unpin, user1["token"], message_1)

# def test_message_unpin():
#     #assert message_unpin(token, message_id) == None
#     assert message_unpin('admin1', 1) == None
#     assert message_unpin('owner', 5) == None

#     def test_basic_case():
#         message_pin('owner', 3)
#         message_unpin('owner', 3)
    
#     with pytest.raises(ValueError):
#     #  message_id is not a valid message within a channel that the authorised user has joined
#         message_unpin('admin1', 78)
#     #  The authorised user is not an admin
#         message_unpin('person1', 1)
#         message_unpin('person2', 3)
#         message_unpin('person3', 1)
#         message_unpin('person3', 2)

#     #  Message with ID message_id is already unpinned
#     def double_unpin():
#         message_pin('admin2', 1)
#         message_unpin('admin2', 1)
#         with pytest.raises(ValueError):
#             message_unpin('admin2', 1)

#     #  The authorised user is not a member of the channel that the message is within
#     def test_error_leave_channel():
#         message_pin('admin1', 1)
#         channel_leave('admin1', 1)
#         with pytest.raises(AccessError) :
#             message_unpin('admin1', 1)
    
