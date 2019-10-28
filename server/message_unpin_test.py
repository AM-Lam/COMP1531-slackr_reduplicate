import pytest
import jwt
from .database import clear_data
from .channel_leave import channel_leave
from .message_unpin import message_unpin
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove
from .message_pin import message_pin
from .access_error import *


def test_message_unpin():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None
    message_pin(user1["token"], message_1['message_id']) 

    assert message_unpin(user1["token"], message_1['message_id']) == {}


def test_no_message():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)
    assert channel_id is not None

    # try to remove a non-existent message
    pytest.raises(ValueError, message_unpin, user1["token"], 123) 
