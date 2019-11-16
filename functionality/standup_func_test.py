# pylint: disable=C0114
# pylint: disable=C0116

import threading
from datetime import timedelta, datetime
import pytest
from .standup import standup_send, standup_start, standup_active
from .auth import auth_register
from .database import clear_data
from .channel import channels_create
from .access_error import AccessError, Value_Error

#######################################################################
###  STANDUP_START TESTS HERE #########################################
#######################################################################

def test_standup_start():
    clear_data()

    user = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "John", "Boe")
    channel = channels_create(user["token"], "Channel 1", False)

    # this test should pass with no issue, to assert just check that the time
    # it returns is within some small range
    dev_time = 5

    predicted_finish_time = datetime.now() + timedelta(seconds=dev_time)
    finish_time = standup_start(user["token"], channel["channel_id"], dev_time)

    assert predicted_finish_time - finish_time <= timedelta(6)

    # returns a Value_Error if the channel doesn't exist
    pytest.raises(Value_Error, standup_start, user["token"],
                  "not_a_real_channel", dev_time)

    # returns an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_start, user2["token"],
                  channel["channel_id"], dev_time)

#######################################################################
###  STANDUP_SEND TESTS HERE ##########################################
#######################################################################

def test_standup_send():
    clear_data()

    dev_time = 5

    user = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "John", "Zoe")

    channel = channels_create(user["token"], "Channel 1", False)

    predicted_finish = datetime.now() + timedelta(seconds=dev_time + 1)

    # start the standup
    threading.Thread(target=standup_start, args=(user["token"],
                     channel["channel_id"], dev_time)).start()

    # this test should pass with no issue
    assert standup_send(user["token"], channel["channel_id"], "message") == {}

    # raises a Value_Error if channel does not exist
    pytest.raises(Value_Error, standup_send, user["token"], "not_a_real_channel", "message")

    # raises an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_send, user2["token"], channel["channel_id"], "message")

    # raises a Value_Error if the message is too long
    pytest.raises(Value_Error, standup_send, user["token"], channel["channel_id"], "a" * 1001)

    # if standup time has stopped
    while datetime.now() <= predicted_finish:
        continue

    pytest.raises(AccessError, standup_send, user["token"], channel["channel_id"], "message")

#######################################################################
###  STANDUP_ACTIVE TESTS HERE ########################################
#######################################################################

def test_standup_active():
    clear_data()

    dev_time = 5

    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    channel = channels_create(user["token"], "Channel 1", False)

    predicted_finish = datetime.now() + timedelta(seconds=dev_time + 1)

    # start the standup
    threading.Thread(target=standup_start, args=(user["token"],
                     channel["channel_id"], dev_time)).start()

    # this test should pass with no issue
    new_standup = standup_active(user["token"], channel["channel_id"])
    assert new_standup["is_active"]
    assert new_standup["time_finish"] - predicted_finish <= timedelta(seconds=1)

    # raises a Value_Error if channel does not exist
    pytest.raises(Value_Error, standup_active, user["token"], "not_a_real_channel")

    # if standup time has stopped
    while datetime.now() <= predicted_finish:
        continue

    assert standup_active(user["token"], channel["channel_id"]) == \
    {"is_active" : False, "time_finish" : None}
