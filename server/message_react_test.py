import pytest
import re
import jwt
from .database import clear_data
from .message_react import message_react
from .auth_register import auth_register
from .message_send import message_send
from .message_remove import message_remove
from .channel import channels_create
from .access_error import *


def test_message_react():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    react_id = 1
    assert message_react(user1["token"], message_1['message_id'], react_id) == {}
                        

def test_no_message():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    message_remove(user1["token"], message_1['message_id'])

    react_id = 1
    # the message is not existed
    pytest.raises(ValueError, message_react, user1["token"], 
                  message_1['message_id'], react_id)
