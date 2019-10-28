import pytest
import jwt
from .database import clear_data
from .auth import auth_register
from .message import message_react, message_remove, message_send, message_unreact
from .channel import channels_create
from .access_error import *


def test_message_unreact():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    react_id = 1
    message_react(user1["token"], message_1['message_id'], react_id)
                        
    assert message_unreact(user1["token"], message_1['message_id'], react_id) == {}


def test_no_message():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    message_remove(user1["token"], message_1['message_id'])

    react_id = 1

    # the message does not exist
    pytest.raises(ValueError, message_unreact, user1["token"], message_1['message_id'], react_id)
