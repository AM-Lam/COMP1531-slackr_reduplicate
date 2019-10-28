import pytest
import jwt
from .database import clear_data
from .auth import auth_register
from .message import message_send
from .channel import channels_create
from .access_error import *


def verify_message(message_obj, correct_data):
    if message_obj == correct_data:
        return True
    return False

def test_message_send():
    clear_data()
    
    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    user2 = auth_register("valid2@email.com", "0123456789", "John", "Bobs")
    user3 = auth_register("valid3@email.com", "0987654321", "Bob", "Zones")
    
    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the channel exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert verify_message(message_1, {"message_id" : 1}) 
    
    # the user is not a member in the group
    pytest.raises(AccessError, message_send, user3["token"],
                  channel_id["channel_id"], "Hello")

    # reset message_1
    message_1 = None
    # the message is over 1000 characters
    pytest.raises(ValueError, message_send, user1["token"],
                  channel_id["channel_id"], "X" * 1001)
