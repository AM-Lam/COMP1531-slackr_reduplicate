# pylint: disable=C0114
# pylint: disable=C0116


from datetime import datetime, timedelta
import pytest
from .database import get_data, clear_data, get_channel, get_user
from .decorators import setup_data
from .auth import auth_register
from .channel import channel_join, channels_create
from .message import (message_edit, message_send, message_remove, message_pin,
                      message_react, message_sendlater, message_unpin,
                      message_unreact, search)
from .access_error import AccessError, Value_Error


# Helper Functions
def get_message_text(channel_id, m_id):
    channel = get_channel(channel_id)
    message = channel.get_message(m_id)
    return message.get_text()


#######################################################################
###  MESSAGE_SEND TESTS HERE #########################################
#######################################################################

# check if the basic functionality of message_send works or not
@setup_data(user_num=2, channel_num=2)
def test_message_send_basic(users, channels):
    # try to create a valid message
    message_1 = message_send(users[0]["token"], channels[0]["channel_id"],
                             "Hello")

    # check that the database was correctly updated
    assert message_1 == {"message_id" : 1}

    # the user is not a member in the group
    pytest.raises(AccessError, message_send, users[1]["token"],
                  channels[0]["channel_id"], "Hello")

    # reset message_1
    message_1 = None
    
    # the message is over 1000 characters
    pytest.raises(Value_Error, message_send, users[0]["token"],
                  channels[0]["channel_id"], "X" * 1001)


#######################################################################
###  MESSAGE_REMOVE TESTS HERE ########################################
#######################################################################


@setup_data(user_num=1, channel_num=1)
def test_message_remove(users, channels):
    # try to create a valid message
    message_1 = message_send(users[0]["token"], channels[0]["channel_id"],
                             "Hello")

    # check that the message exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert message_remove(users[0]["token"], message_1['message_id']) == {}


@setup_data(user_num=2, channel_num=1)
def test_invalid_user(users, channels):
    channel_join(users[1]["token"], channels[0]["channel_id"])
    message_1 = message_send(users[0]["token"], channels[0]["channel_id"],
                             "Hello")


    # try to remove a message you did not send
    pytest.raises(AccessError, message_remove, users[1]["token"], message_1['message_id'])


@setup_data(user_num=2, channel_num=1)
def test_admin_user(users, channels):
    user2_obj = get_user(users[1]["u_id"])
    user2_obj.set_global_admin(True)

    channel = channels_create(users[0]["token"], "Channel 1", True)
    message_1 = message_send(users[0]["token"], channel["channel_id"], "Hello")

    # delete the message
    assert message_remove(users[1]["token"], message_1['message_id']) == {}


#######################################################################
###  MESSAGE_EDIT TESTS HERE ##########################################
#######################################################################

@setup_data(user_num=2, channel_num=1)
def test_message_edit(users, channels):
    user2_obj = get_user(users[1]["u_id"])

    channel_join(users[1]["token"], channels[0]["channel_id"])

    message1 = message_send(users[0]["token"], channels[0]["channel_id"],
                            "Hello")

    message2 = message_send(users[1]["token"], channels[0]["channel_id"],
                            "Google Murray Bookchin")

    # edit a message we created, and check that it updated correctly
    assert message_edit(users[0]["token"], message1['message_id'], "Hi") == {}
    
    assert get_message_text(channels[0]["channel_id"],
                            message1["message_id"]) == "Hi"

    # try to edit a message we did not send as a regular user
    pytest.raises(AccessError, message_edit, users[1]["token"],
                  message1['message_id'], "Heeeello")

    # try to edit a message we did not send as an owner
    assert message_edit(users[0]["token"],
                        message2['message_id'], "Chomsky is good") == {}
    
    assert get_message_text(channels[0]["channel_id"],
                            message2["message_id"]) == "Chomsky is good"

    # try to edit a message that does not exist
    pytest.raises(Value_Error, message_edit, users[0]["token"], 10101,
                  "Hello There")

    # try to edit a message we do not own as a global admin
    user2_obj.set_global_admin(True)

    assert message_edit(users[1]["token"], message1['message_id'],
                        "Heeeello") == {}
    assert get_message_text(channels[0]["channel_id"],
                            message1["message_id"]) == "Heeeello"


#######################################################################
###  MESSAGE_PIN TESTS HERE ###########################################
#######################################################################


@setup_data(user_num=2, channel_num=1)
def test_message_pin(users, channels):
    channel_join(users[1]["token"], channels[0]["channel_id"])

    # try to create a valid message
    message1 = message_send(users[0]["token"], channels[0]["channel_id"],
                             "Hello")
    
    message2 = message_send(users[1]["token"], channels[0]["channel_id"],
                             "Hi")

    assert message_pin(users[0]["token"], message1['message_id']) == {}

    # try to pin a message that is already pinned
    pytest.raises(Value_Error, message_pin, users[0]["token"],
                  message1["message_id"])
    
    # try to pin a message as a regular user
    pytest.raises(Value_Error, message_pin, users[1]["token"],
                  message2["message_id"])


#######################################################################
###  MESSAGE_UNPIN TESTS HERE #########################################
#######################################################################


@setup_data(user_num=2, channel_num=1)
def test_message_unpin(users, channels):
    channel_join(users[1]["token"], channels[0]["channel_id"])
    
    message1 = message_send(users[0]["token"], channels[0]["channel_id"],
                             "Hello")

    message_pin(users[0]["token"], message1['message_id'])
    
    assert message_unpin(users[0]["token"], message1['message_id']) == {}

    # try to unpin a message that is not pinned
    pytest.raises(Value_Error, message_unpin, users[0]["token"],
                  message1["message_id"])

    message_pin(users[0]["token"], message1['message_id'])
    
    # try to unpin a pinned message as a regular user
    pytest.raises(Value_Error, message_unpin, users[1]["token"],
                  message1["message_id"])

#######################################################################
###  MESSAGE_REACT TESTS HERE #########################################
#######################################################################


@setup_data(user_num=2, channel_num=1)
def test_message_react(users, channels):
    channel_join(users[1]["token"], channels[0]["channel_id"])

    # try to create a valid message
    message1 = message_send(users[0]["token"], channels[0]["channel_id"],
                             "Hello")
    react_id = 1
    
    assert message_react(users[0]["token"], message1['message_id'],
                         react_id) == {}
    
    # add the same react to the same message from a different user
    assert message_react(users[1]["token"], message1['message_id'],
                         react_id) == {}
    
    # add a different react to the same message
    assert message_react(users[1]["token"], message1['message_id'],
                         2) == {}
    
    # try to react to a message that we have already reacted to, with
    # the same react
    pytest.raises(Value_Error, message_react, users[1]["token"],
                  message1['message_id'], react_id)


#######################################################################
###  MESSAGE_UNREACT TESTS HERE #######################################
#######################################################################


@setup_data(user_num=1, channel_num=1)
def test_message_unreact(users, channels):
    # try to create a valid message
    message_1 = message_send(users[0]["token"], channels[0]["channel_id"],
                             "Hello")
    react_id = 1
    
    message_react(users[0]["token"], message_1['message_id'], 2)
    message_react(users[0]["token"], message_1['message_id'], 3)
    message_react(users[0]["token"], message_1['message_id'], 1)    
    
    assert message_unreact(users[0]["token"], message_1['message_id'],
                           react_id) == {}
    
    # try to unreact a message that we have not reacted to
    pytest.raises(Value_Error, message_unreact, users[0]["token"],
                  message_1['message_id'], react_id)
    
    # try to unreact from a message that does not exist
    pytest.raises(Value_Error, message_unreact, users[0]["token"],
                  message_1['message_id'], 4)


#######################################################################
###  MESSAGE_SENDLATER TESTS HERE #####################################
#######################################################################


@setup_data(user_num=2, channel_num=1)
def test_message_sendlater(users, channels):
    # get the channel object, we need this to check if messages were sent
    channel_obj = get_channel(channels[0]["channel_id"])

    # first test some cases that should raise exceptions
    # message > 1000 characters
    pytest.raises(Value_Error, message_sendlater, users[0]["token"],
                  channels[0]["channel_id"], "X" * 1001,
                  datetime.now() + timedelta(minutes=1))

    # time sent is in the past
    pytest.raises(Value_Error, message_sendlater, users[0]["token"],
                  channels[0]["channel_id"], "Message", datetime(2000, 1, 1))

    # non-existent channel
    pytest.raises(Value_Error, message_sendlater, users[0]["token"],
                  404, "Message", datetime.now() + timedelta(minutes=1))

    # now try to send a valid message in the future
    time_sent = datetime.utcnow() + timedelta(seconds=5)
    assert message_sendlater(users[0]["token"], channels[0]["channel_id"], "Message",
                             time_sent) == {"message_id" : 1}

    # ensure that the message has not yet appeared
    assert len(channel_obj.get_messages()) == 0

    # wait until the time has passed then check if the message was sent
    # (wait a little longer just to ensure that we aren't checking for the
    # message at the same time as it is sent)
    while datetime.utcnow() < time_sent + timedelta(seconds=1):
        continue

    assert len(channel_obj.get_messages()) == 1

    # try to send a message in a channel we do not have access to
    time_sent = datetime.utcnow() + timedelta(seconds=5)
    pytest.raises(AccessError, message_sendlater, users[1]["token"],
                  channels[0]["channel_id"], "message", time_sent)


#######################################################################
###  MESSAGE_SEARCH TESTS HERE ########################################
#######################################################################


@setup_data(user_num=3, channel_num=2, creators=[0, 1], public=[True, False])
def test_search_basic(users, channels):
    # try to create a valid message
    message_send(users[0]["token"], channels[0]["channel_id"], "hello there")
    
    # try to create a message in a private chat
    message_send(users[1]["token"], channels[1]["channel_id"], "whats this")

    # just checking for message length right now because it's faster
    # find all the matching messages
    assert len(search(users[0]["token"], "hello")["messages"]) == 1

    # users[2] does not have access so they can't access the messages,
    # (users[0] does as they are a global admin)
    assert len(search(users[2]["token"], "this")["messages"]) == 0

    # but users[1] can access those messages
    assert len(search(users[1]["token"], "this")["messages"]) == 1

    # return nothing if the query string is in no messages
    assert len(search(users[0]["token"], "xxx")["messages"]) == 0

    # if query string is a space, return almost anything
    assert len(search(users[1]["token"], " ")["messages"]) == 1

    # check that a global admin can access messages in all channels
    assert len(search(users[0]["token"], " ")["messages"]) == 2


@setup_data(user_num=1, channel_num=1)
def test_no_message(users, channels):
    # try to create a valid message
    message_1 = message_send(users[0]["token"], channels[0]["channel_id"], "Hello")
    assert message_1 is not None

    # check that you can remove the message
    assert message_remove(users[0]["token"], message_1['message_id']) == {}

    # check that you cannot remove a message that no longer exists
    pytest.raises(Value_Error, message_remove, users[0]["token"],
                  message_1['message_id'])

    # check that you cannot pin a message that no longer exists
    pytest.raises(Value_Error, message_pin, users[0]["token"],
                  message_1['message_id'])

    # try to unpin a non-existent message
    pytest.raises(Value_Error, message_unpin, users[0]["token"], 123)

    react_id = 1
    # check that you cannot react a message that no longer exists
    pytest.raises(Value_Error, message_react, users[0]["token"],
                  message_1['message_id'], react_id)

    # try to unreact a non-existent message
    pytest.raises(Value_Error, message_unreact, users[0]["token"],
                  message_1['message_id'], react_id)
