import pytest
import jwt
from .database import *
from .access_error import *
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove

def test_message_remove():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    secret = get_secret()
    user1 = {
        "token" : jwt.encode({"u_id" : "111"}, secret, algorithm="HS256").decode(),
        "u_id" : "111"
    }

    user2 = {
        "token" : jwt.encode({"u_id" : "22"}, secret, algorithm="HS256").decode(),
        "u_id" : "22"
    }

    user3 = {
        "token" : jwt.encode({"u_id" : "3"}, secret, algorithm="HS256").decode(),
        "u_id" : "3"
    }

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None

    message_remove(user1["token"], message_1)
    # check that the database was correctly updated
    assert message_1 is None

def test_no_message():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }

    channel_id = channels_create(user1["token"], "Channel 1", True)

    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    assert message_1 is not None

    message_remove(user1["token"], message_1)

    # check that the channel exists
    assert message_1 is None

    # the message is no longer existed
    pytest.raises(ValueError, message_remove, user1["token"], message_1)


def test_invalid_user():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    secret = get_secret()
    user1 = {
        "token" : jwt.encode({"u_id" : "111"}, secret, algorithm="HS256").decode(),
        "u_id" : "111"
    }

    user2 = {
        "token" : jwt.encode({"u_id" : "22"}, secret, algorithm="HS256").decode(),
        "u_id" : "22"
    }

    user3 = {
        "token" : jwt.encode({"u_id" : "3"}, secret, algorithm="HS256").decode(),
        "u_id" : "3"
    }

    channel_id = channels_create(user1["token"], "Channel 1", True)

    db = get_data()
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    
    # check that the channel exists
    assert message_1 is not None
    pytest.raises(AccessError, message_remove, user3["token"], message_1)

def test_admin_user():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    secret = get_secret()
    user1 = {
        "token" : jwt.encode({"u_id" : "111"}, secret, algorithm="HS256").decode(),
        "u_id" : "111"
    }

    user2 = {
        "token" : jwt.encode({"u_id" : "22"}, secret, algorithm="HS256").decode(),
        "u_id" : "22"
    }

    user3 = {
        "token" : jwt.encode({"u_id" : "3"}, secret, algorithm="HS256").decode(),
        "u_id" : "3"
    }


    channel_id = channels_create(user1["token"], "Channel 1", True)

    db = get_data()
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    # check that the message exists
    assert message_1 is not None
    message_remove(user1["token"], message_1)

    # message is no longer existed
    assert message_1 is None

    # # sender remove the message 
    # assert message_remove('person1', 1) == None
    # assert message_remove('person2', 3) == None

    # #admin remove the message
    # assert message_remove('admin1', 5) == None

    # # Message is not existed
    # with pytest.raises(ValueError):
    #     message_remove('owner', 45)
    #     message_remove('person1', 123)

    # # Message (based on ID) no longer exists
    # def test_message_no_longer_exist():
    #     # remove the message first
    #     message_send('person1', 1, 'a')
    #     message_remove('person1', 1)
    #     # Now the message is no longer exists
    #     with pytest.raises(ValueError):
    #         message_remove('person1', 1)

    # # AccessError: 
    # # if user is not a member of a certain channel anymore
    # def test_error_leave_channel():
    #     channel_leave('person1', 1)
    #     with pytest.raises(AccessError) :
    #         message_remove('person1', 1)

    # # Admin of channel A is not channel B but they try to delete message in channel B
    # with pytest.raises(AccessError): 
    #     message_remove('admin1', 2)
    #     message_remove('admin2', 3)

    # # admin of other channel but not even a member in channel_id
    # with pytest.raises(AccessError):
    #     message_remove('admin2', 1)
    #     message_remove('admin1', 3)
