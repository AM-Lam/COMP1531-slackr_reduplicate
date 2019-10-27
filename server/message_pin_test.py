import pytest
import jwt
from .access_error import *
from .database import *
from .message_pin import message_pin
from .channel_leave import channel_leave
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove

def test_message_pin():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None
    
    assert message_pin(user1["token"], message_1['message_id']) == {}

def test_no_message1():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    # message is not existed anymore
    message_remove(user1["token"], message_1['message_id'])

    # the message is not existed
    pytest.raises(ValueError, message_pin, user1["token"], message_1['message_id'])

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
    
