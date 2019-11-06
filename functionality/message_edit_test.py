import pytest
import jwt
from .database import get_data, clear_data
from .auth import auth_register
from .channel import channel_join, channels_create
from .message import message_edit, message_send, message_remove
from .access_error import AccessError, Value_Error


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
    pytest.raises(Value_Error, message_edit, user1["token"], 
                  10101, "Hello There")
    
    # try to edit a message we do not own as a global admin
    user2_obj.set_global_admin(True)

    assert message_edit(user2["token"], message1['message_id'], "Heeeello") == {}
    assert get_message_text(message1["message_id"]) == "Heeeello"

# if the message string is empty, the message will be deleted
def test_empty_message():
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

    # edit a message we created to an empty string, and check that it is deleted
    assert message_edit(user1["token"], message1['message_id'], "") == {}

    # try to edit a message that does not exist
    pytest.raises(Value_Error, message_edit, user1["token"], 
                   message1['message_id'], "Hello There")