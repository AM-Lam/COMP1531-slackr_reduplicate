import pytest
import jwt
from .database import clear_data
from .auth import auth_register
from .message import message_remove, message_send, message_pin
from .channel import channels_create, channel_leave
from .access_error import AccessError, Value_Error


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
    pytest.raises(Value_Error, message_pin, user1["token"], message_1['message_id'])
