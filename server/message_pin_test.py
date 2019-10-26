import pytest
from .database import *
from .auth_register import auth_register
from .channels_create import channels_create
from .message_pin import message_pin

def test_message_pin():
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

    # check that the message exists
    assert message_1 is not None
    message_pin(user1["token"], message_1)
    assert db['message'][0]._pinned == True

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
    pytest.raises(ValueError, message_pin, user1["token"], message_1)

    # # assert message_pin(token, message_id) == None
    # assert message_pin('admin1', 1) == None
    # assert message_pin('admin1', 5) == None
    # assert message_pin('admin2', 2) == None
    # assert message_pin('owner', 3) == None
    # assert message_pin('owner', 4) == None

    # with pytest.raises(ValueError):
    # #  message_id is not a valid message within a channel that the authorised user has joined
    #     message_pin('admin1', 456)

    # #  The authorised user is not an admin
    #     message_pin('admin1', 3)
    #     message_pin('admin1', 4)
    #     message_pin('admin2', 1)

    # #  Message with ID message_id is already pinned
    # def double_pin():
    #     message_pin('admin2', 2)
    #     with pytest.raises(ValueError):
    #         message_pin('admin2', 2)

    # #  The authorised user is not a member of the channel that the message is within
    # def test_error_leave_channel():
    #     channel_leave('admin2', 3)
    #     with pytest.raises(AccessError):
    #         message_pin('admin2', 2)
    
