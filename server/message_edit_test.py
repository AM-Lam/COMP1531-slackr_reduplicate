import pytest
import jwt
from .database import get_data, clear_data
from .auth_register import auth_register
from .message_send import message_send
from .message_remove import message_remove
from .message_edit import message_edit
from .channel import channel_join, channels_create
from .access_error import *


def verify_message(message_obj, correct_data):
    if message_obj == correct_data:
        return True
    return False


def get_message_text(m_id):
    server_data = get_data()

    for c in server_data["channels"]:
        for m in c.get_messages():
            if m.get_m_id() == m_id: 
                return m.get_text()


def test_message_edit():
    clear_data()

    server_data = get_data()
    
    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    user2 = auth_register("valid2@email.com", "1234567890", "Bob", "Zones")

    user2_obj = None
    for u in server_data["users"]:
        if u.get_u_id() == user2["u_id"]:
            user2_obj = u
            break
    
    channel = channels_create(user1["token"], "Channel 1", True)
    channel_join(user2["token"], channel["channel_id"])

    message1 = message_send(user1["token"], channel["channel_id"], "Hello")
    message2 = message_send(user2["token"], channel["channel_id"], "Google Murray Bookchin")
    
    # edit a message we created, and check that it updated correctly
    assert message_edit(user1["token"], message1['message_id'], "Hi") == {}
    assert get_message_text(message1["message_id"]) == "Hi"

    # try to edit a message we did not send as a regular user
    pytest.raises(AccessError, message_edit, user2["token"], 
                  message1['message_id'], "Heeeello")

    # try to edit a message we did not send as an owner
    assert message_edit(user1["token"], message2['message_id'], "Chomsky is good") == {}
    assert get_message_text(message2["message_id"]) == "Chomsky is good"

    # try to edit a message that does not exist
    pytest.raises(ValueError, message_edit, user1["token"], 
                  10101, "Hello There")
    
    # try to edit a message we do not own as a global admin
    user2_obj.set_global_admin(True)

    assert message_edit(user2["token"], message1['message_id'], "Heeeello") == {}
    assert get_message_text(message1["message_id"]) == "Heeeello"
