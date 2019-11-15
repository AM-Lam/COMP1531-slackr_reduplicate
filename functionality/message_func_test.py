# pylint: disable=C0114
# pylint: disable=C0116


from datetime import datetime, timedelta
import pytest
from .database import get_data, clear_data, get_channel
from .auth import auth_register
from .channel import channel_join, channels_create, channel_removeowner
from .message import (message_edit, message_send, message_remove, message_pin,
                      message_react, message_sendlater, message_unpin,
                      message_unreact, search)
from .access_error import AccessError, Value_Error
from .decorators import setup_data


# Helper Functions

def get_message_text(channel_id, m_id):
    channel = get_channel(channel_id)
    message = channel.get_message(m_id)
    return message.get_text()

#######################################################################
###  MESSAGE_SEND TESTS HERE #########################################
#######################################################################

# check if the basic functionality of message_send works or not
@setup_data(user_num=2, channel_num=1)
def test_message_send_basic(users, channels):

    user1 = users[0]["token"]
    user2 = users[1]["token"]
    channel_id = channels[0]["channel_id"]

    # try to create a valid message
    message_1 = message_send(user1, channel_id, "Hello")

    # check that the channel exists
    assert message_1 is not None

    # the user is not a member in the group
    pytest.raises(AccessError, message_send, user2,
                  channel_id, "Hello")

    # reset message_1
    message_1 = None
    # the message is over 1000 characters
    pytest.raises(Value_Error, message_send, user1,
                  channel_id, "X" * 1001)


#######################################################################
###  MESSAGE_REMOVE TESTS HERE ########################################
#######################################################################
# check if the basic functionality of message_remove works or not
@setup_data(user_num=1, channel_num=1)
def test_message_remove(users, channels):
    user1 = users[0]["token"]
    channel_id = channels[0]["channel_id"]

    # try to create a valid message
    message_1 = message_send(user1, channel_id, "Hello")

    # check that the message exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert message_remove(user1, message_1['message_id']) == {}

# put up an error when user who is not a poster try to remove the message
@setup_data(user_num=2, channel_num=1)
def test_invalid_user(users, channels):
    
    user1 = users[0]["token"]
    user2 = users[1]["token"]
    channel = channels[0]["channel_id"]

    # when user2 is a member of the group
    channel_join(user2, channel)

    message_1 = message_send(user1, channel, "Hello")

    # check that the message exists
    assert message_1 is not None

    # try to remove a message you did not send
    pytest.raises(AccessError, message_remove, user2, message_1['message_id'])

# request send by an admin who isn't the poster
@setup_data(user_num=2)
def test_admin_user(users, channels):
    server_data = get_data()

    user1 = users[0]
    user2 = users[1]

    user1_obj = server_data["users"][user1["u_id"]]
    user1_obj.set_global_admin(True)

    channel = channels_create(user2["token"], "Channel 1", True)

    message_1 = message_send(user2["token"], channel["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None

    # delete the message
    assert message_remove(user1["token"], message_1['message_id']) == {}


#######################################################################
###  MESSAGE_EDIT TESTS HERE ##########################################
#######################################################################

# check if the basic functionality of message_edit works or not
@setup_data(user_num=2, channel_num=1)
def test_message_edit_basic(users, channels):
    user1 = users[0]
    user2 = users[1]

    server_data = get_data()
    user2_obj = server_data["users"][user2["u_id"]]

    channel = channels[0]["channel_id"]
    channel_join(user2["token"], channel)

    message1 = message_send(user1["token"], channel, "Hello")
    message2 = message_send(user2["token"], channel, "Google Murray Bookchin")

    # edit a message we created, and check that it updated correctly
    assert message_edit(user1["token"], message1['message_id'], "Hi") == {}
    assert get_message_text(channel, message1["message_id"]) == "Hi"

    # try to edit a message we did not send as a regular user
    pytest.raises(AccessError, message_edit, user2["token"],
                  message1['message_id'], "Heeeello")

    # try to edit a message we did not send as an owner
    assert message_edit(user1["token"], message2['message_id'], "Chomsky is good") == {}
    assert get_message_text(channel, message2["message_id"]) == "Chomsky is good"

    # try to edit a message that does not exist
    pytest.raises(Value_Error, message_edit, user1["token"], 10101,
                  "Hello There")

    # # non-existent channel
    # pytest.raises(Value_Error, message_edit, user1["token"], message1['message_id'], "Message")

    # try to edit a message we do not own as a global admin
    user2_obj.set_global_admin(True)

    assert message_edit(user2["token"], message1['message_id'], "Heeeello") == {}
    assert get_message_text(channel, message1["message_id"]) == "Heeeello"


#######################################################################
###  MESSAGE_PIN TESTS HERE ###########################################
#######################################################################
# check if the basic functionality of message_pin works or not
@setup_data(user_num=1, channel_num=1)
def test_message_pin(users, channels):

    user1 = users[0]["token"]
    channel_id = channels[0]["channel_id"]
    
    # try to create a valid message
    message_1 = message_send(user1, channel_id, "Hello")

    # check that the message exists
    assert message_1 is not None

    assert message_pin(user1, message_1['message_id']) == {}

    # the message is pinned
    pytest.raises(Value_Error, message_pin, user1, message_1['message_id'])

#######################################################################
###  MESSAGE_UNPIN TESTS HERE #########################################
#######################################################################
# check if the basic functionality of message_unpin works or not
@setup_data(user_num=2, channel_num=1)
def test_message_unpin_basic(users, channels):
    user1 = users[0]["token"]
    user2 = users[1]["token"]
    channel_id = channels[0]["channel_id"]

    # try to create a valid message
    message_1 = message_send(user1, channel_id, "Hello")

    # the message cannot be unpin if it is not pinned
    pytest.raises(Value_Error, message_unpin, user1, message_1)

    # check that the message exists
    assert message_1 is not None
    message_pin(user1, message_1['message_id'])

    assert message_unpin(user1, message_1['message_id']) == {}

@setup_data(user_num=2, channel_num=1)
def test_message_unpin_not_admin(users, channels):
    user1 = users[0]
    user2 = users[1]["token"]
    channel_id = channels[0]["channel_id"]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id, "Hello")

    # the message cannot be unpin if it is not pinned
    pytest.raises(Value_Error, message_unpin, user1["token"], message_1)

    # check that the message exists
    assert message_1 is not None
    message_pin(user1["token"], message_1['message_id'])

    channel_removeowner(user1["token"], channel_id, user1["u_id"])
    # the user is not an admin in the group
    pytest.raises(Value_Error, message_unpin, user1["token"], message_1['message_id'])

#######################################################################
###  MESSAGE_REACT TESTS HERE #########################################
#######################################################################
# check if the basic functionality of message_react works or not
@setup_data(user_num=1, channel_num=1)
def test_message_react_basic(users, channels):

    user1 = users[0]["token"]
    channel_id = channels[0]["channel_id"]

    # try to create a valid message
    message_1 = message_send(user1, channel_id, "Hello")

    react_id = 1
    assert message_react(user1, message_1["message_id"], react_id) == {}


#######################################################################
###  MESSAGE_UNREACT TESTS HERE #######################################
#######################################################################
# check if the basic functionality of message_send works or not
@setup_data(user_num=1, channel_num=1)
def test_message_unreact_basic(users, channels):

    user1 = users[0]["token"]
    channel_id = channels[0]["channel_id"]

    # try to create a valid message
    message_1 = message_send(user1, channel_id, "Hello")

    react_id = 1
    message_react(user1, message_1['message_id'], react_id)

    assert message_unreact(user1, message_1['message_id'], react_id) == {}


#######################################################################
###  MESSAGE_SENDLATER TESTS HERE #####################################
#######################################################################
# check if the basic functionality of message_send works or not
@setup_data(user_num=2, channel_num=1)
def test_message_sendlater(users, channels):

    user1 = users[0]["token"]
    user2 = users[1]["token"]
    channel = channels[0]["channel_id"]

    server_data = get_data()

    # get the channel object, we need this to check if messages were sent
    channel_obj = server_data["channels"][channel]

    # first test some cases that should raise exceptions
    # message > 1000 characters
    pytest.raises(Value_Error, message_sendlater, user1,
                  channel, "X" * 1001,
                  datetime.now() + timedelta(minutes=1))

    # user is not a member in the channel
    pytest.raises(AccessError, message_sendlater, user2,
                   channel, "Message", datetime.now() + timedelta(minutes=1))

    # time sent is in the past
    pytest.raises(Value_Error, message_sendlater, user1,
                  channel, "Message", datetime(2000, 1, 1))

    # non-existent channel
    pytest.raises(Value_Error, message_sendlater, user1,
                  404, "Message", datetime.now() + timedelta(minutes=1))

    # now try to send a valid message in the future
    time_sent = datetime.utcnow() + timedelta(seconds=5)
    assert message_sendlater(user1, channel, "Message",
                             time_sent) == {"message_id" : 1}

    # ensure that the message has not yet appeared
    assert len(channel_obj.get_messages()) == 0


    # wait until the time has passed then check if the message was sent
    # (wait a little longer just to ensure that we aren't checking for the
    # message at the same time as it is sent)
    while datetime.utcnow() < time_sent + timedelta(seconds=1):
        continue

    assert len(channel_obj.get_messages()) == 1

#######################################################################
###  MESSAGE_SEARCH TESTS HERE ########################################
#######################################################################
# check if the basic functionality of message_send works or not
@setup_data(user_num=1)
def test_search_basic(users, channels):
    user = users[0]["token"]

    # find all the matching messages (nothing)
    assert search(user, "hewwo") == []

    # return nothing if the query string is nothing
    assert search(user, "") == []

# common test case applied to more than one fucntion
@setup_data(user_num=1, channel_num=1)
def test_no_message(users, channels):
    user1 = users[0]["token"]
    channel_id = channels[0]["channel_id"]

    # try to create a valid message
    message_1 = message_send(user1, channel_id, "Hello")
    assert message_1 is not None

    # check that you can remove the message
    assert message_remove(user1, message_1['message_id']) == {}

    # check that you cannot remove a message that no longer exists
    pytest.raises(Value_Error, message_remove, user1, message_1['message_id'])

    # check that you cannot pin a message that no longer exists
    pytest.raises(Value_Error, message_pin, user1, message_1['message_id'])

    # try to unpin a non-existent message
    pytest.raises(Value_Error, message_unpin, user1, 123)

    react_id = 1
    # check that you cannot react a message that no longer exists
    pytest.raises(Value_Error, message_react, user1,
                  message_1['message_id'], react_id)

    # try to unreact a non-existent message
    pytest.raises(Value_Error, message_unreact, user1, message_1['message_id'], react_id)
