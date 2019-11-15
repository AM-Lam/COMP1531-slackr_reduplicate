# pylint: disable=C0114
# pylint: disable=C0116


from datetime import datetime, timedelta
import pytest
from .database import get_data, clear_data, get_channel
from .auth import auth_register
from .channel import channel_join, channels_create
from .message import (message_edit, message_send, message_remove, message_pin,
                      message_react, message_sendlater, message_unpin,
                      message_unreact, search)
from .access_error import AccessError, Value_Error


# Helper Functions

# check if the message is valid
def verify_message(message_obj, correct_data):
    if message_obj == correct_data:
        return True
    return False


def get_message_text(channel_id, m_id):
    channel = get_channel(channel_id)
    message = channel.get_message(m_id)
    return message.get_text()

# put all the setup like create account and channel for the test in this function
def setup():
    clear_data()

    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    user2 = auth_register("valid2@email.com", "0123456789", "John", "Bobs")
    yield user1
    yield user2

    # create the channel we test with
    channel_id = channels_create(user1["token"], "Channel 1", True)
    yield channel_id

#######################################################################
###  MESSAGE_SEND TESTS HERE #########################################
#######################################################################

# check if the basic functionality of message_send works or not
def test_message_send_basic():

    set_up = list(setup())
    user1 = set_up[0]
    user2 = set_up[1]
    channel_id = set_up[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the channel exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert verify_message(message_1, {"message_id" : 1})

    # the user is not a member in the group
    pytest.raises(AccessError, message_send, user2["token"],
                  channel_id["channel_id"], "Hello")

    # reset message_1
    message_1 = None
    # the message is over 1000 characters
    pytest.raises(Value_Error, message_send, user1["token"],
                  channel_id["channel_id"], "X" * 1001)


#######################################################################
###  MESSAGE_REMOVE TESTS HERE ########################################
#######################################################################

def test_message_remove():
    clear_data()

    setup1 = list(setup())
    user1 = setup1[0]
    channel_id = setup1[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert message_remove(user1["token"], message_1['message_id']) == {}

def test_no_message9():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    assert message_1 is not None

    # check that you can remove the message
    assert message_remove(user1["token"], message_1['message_id']) == {}

    # check that you cannot remove a message that no longer exists
    pytest.raises(Value_Error, message_remove, user1["token"], message_1['message_id'])

def test_invalid_user10():
    
    set_up = list(setup())
    user1 = set_up[0]
    user2 = set_up[1]
    channel = set_up[2]

    channel_join(user2["token"], channel["channel_id"])

    message_1 = message_send(user1["token"], channel["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None

    # try to remove a message you did not send
    pytest.raises(AccessError, message_remove, user2["token"], message_1['message_id'])


def test_admin_user11():
    set_up = list(setup())
    server_data = get_data()

    user1 = set_up[0]
    user2 = set_up[1]

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


def test_message_edit():
    set_up = list(setup())
    user1 = set_up[0]
    user2 = set_up[1]

    server_data = get_data()
    user2_obj = server_data["users"][user2["u_id"]]

    channel = set_up[2]
    channel_join(user2["token"], channel["channel_id"])

    message1 = message_send(user1["token"], channel["channel_id"], "Hello")
    message2 = message_send(user2["token"], channel["channel_id"], "Google Murray Bookchin")

    # edit a message we created, and check that it updated correctly
    assert message_edit(user1["token"], message1['message_id'], "Hi") == {}
    assert get_message_text(channel["channel_id"], message1["message_id"]) == "Hi"

    # try to edit a message we did not send as a regular user
    pytest.raises(AccessError, message_edit, user2["token"],
                  message1['message_id'], "Heeeello")

    # try to edit a message we did not send as an owner
    assert message_edit(user1["token"], message2['message_id'], "Chomsky is good") == {}
    assert get_message_text(channel["channel_id"], message2["message_id"]) == "Chomsky is good"

    # try to edit a message that does not exist
    pytest.raises(Value_Error, message_edit, user1["token"], 10101,
                  "Hello There")

    # try to edit a message we do not own as a global admin
    user2_obj.set_global_admin(True)

    assert message_edit(user2["token"], message1['message_id'], "Heeeello") == {}
    assert get_message_text(channel["channel_id"], message1["message_id"]) == "Heeeello"


#######################################################################
###  MESSAGE_PIN TESTS HERE ###########################################
#######################################################################

def test_message_pin4():

    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]
    
    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None

    assert message_pin(user1["token"], message_1['message_id']) == {}


def test_no_message15():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    # message is not existed anymore
    message_remove(user1["token"], message_1['message_id'])

    # the message does not exist
    pytest.raises(Value_Error, message_pin, user1["token"], message_1['message_id'])


#######################################################################
###  MESSAGE_UNPIN TESTS HERE #########################################
#######################################################################

def test_message_unpin14():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None
    message_pin(user1["token"], message_1['message_id'])

    assert message_unpin(user1["token"], message_1['message_id']) == {}


def test_no_message16():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    assert channel_id is not None

    # try to remove a non-existent message
    pytest.raises(Value_Error, message_unpin, user1["token"], 123)

#######################################################################
###  MESSAGE_REACT TESTS HERE #########################################
#######################################################################

def test_message_react6():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    react_id = 1
    assert message_react(user1["token"], message_1['message_id'], react_id) == {}


def test_no_message7():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    message_remove(user1["token"], message_1['message_id'])

    react_id = 1
    # the message is not existed
    pytest.raises(Value_Error, message_react, user1["token"],
                  message_1['message_id'], react_id)



#######################################################################
###  MESSAGE_UNREACT TESTS HERE #######################################
#######################################################################

def test_message_unreact16():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    react_id = 1
    message_react(user1["token"], message_1['message_id'], react_id)

    assert message_unreact(user1["token"], message_1['message_id'], react_id) == {}


def test_no_message17():
    set_up = list(setup())
    user1 = set_up[0]
    channel_id = set_up[2]

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    message_remove(user1["token"], message_1['message_id'])

    react_id = 1

    # the message does not exist
    pytest.raises(Value_Error, message_unreact, user1["token"], message_1['message_id'], react_id)



#######################################################################
###  MESSAGE_SENDLATER TESTS HERE #####################################
#######################################################################

def test_message_sendlater13():
    set_up = list(setup())
    user1 = set_up[0]
    channel1 = set_up[2]

    server_data = get_data()

    # get the channel object, we need this to check if messages were sent
    channel_obj = server_data["channels"][channel1["channel_id"]]

    # first test some cases that should raise exceptions
    # message > 1000 characters
    pytest.raises(Value_Error, message_sendlater, user1["token"],
                  channel1["channel_id"], "X" * 1001,
                  datetime.now() + timedelta(minutes=1))

    # time sent is in the past
    pytest.raises(Value_Error, message_sendlater, user1["token"],
                  channel1["channel_id"], "Message", datetime(2000, 1, 1))

    # non-existent channel
    pytest.raises(Value_Error, message_sendlater, user1["token"],
                  404, "Message", datetime.now() + timedelta(minutes=1))

    # now try to send a valid message in the future
    time_sent = datetime.utcnow() + timedelta(seconds=5)
    assert message_sendlater(user1["token"], channel1["channel_id"], "Message",
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

def test_search18():
    set_up = list(setup())
    user = set_up[0]

    # find all the matching messages (nothing)
    assert search(user["token"], "hewwo") == []

    # return nothing if the query string is nothing
    assert search(user["token"], "") == []
