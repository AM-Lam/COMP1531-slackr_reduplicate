import pytest
import jwt
from .database import clear_data, get_data
from .auth import auth_register
from .message import message_send, message_remove
from .channel import channels_create, channel_join
from .access_error import *


def test_message_remove():
    clear_data()
    
    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert message_remove(user1["token"], message_1['message_id']) == {}

def test_no_message():
    clear_data()
    
    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    channel_id = channels_create(user1["token"], "Channel 1", True)

    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    assert message_1 is not None

    # check that you can remove the message
    assert message_remove(user1["token"], message_1['message_id']) == {}

    # check that you cannot remove a message that no longer exists
    pytest.raises(ValueError, message_remove, user1["token"], message_1['message_id'])

def test_invalid_user():
    clear_data()

    server_data = get_data()

    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    user2 = auth_register("valid2@email.com", "0987654321", "James", "Bones")

    # user1_obj = server_data["users"][0]
    # user1_obj.set_global_admin(True)

    channel = channels_create(user1["token"], "Channel 1", True)
    channel_join(user2["token"], channel["channel_id"])

    message_1 = message_send(user1["token"], channel["channel_id"], "Hello")
    
    # check that the message exists
    assert message_1 is not None

    # try to remove a message you did not send
    pytest.raises(AccessError, message_remove, user2["token"], message_1['message_id'])


def test_admin_user():
    clear_data()

    server_data = get_data()

    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    user2 = auth_register("valid2@email.com", "0987654321", "James", "Bones")

    user1_obj = server_data["users"][0]
    user1_obj.set_global_admin(True)

    channel = channels_create(user2["token"], "Channel 1", True)
    # channel_join(user2["token"], channel["channel_id"])

    message_1 = message_send(user2["token"], channel["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None
    
    # delete the message
    assert message_remove(user1["token"], message_1['message_id']) == {}
