# pylint: disable=C0114
# pylint: disable=C0116

import threading
from datetime import timedelta, datetime
import pytest
from .standup import standup_send, standup_start, standup_active
from .access_error import AccessError, Value_Error
from .decorators import setup_data

#######################################################################
###  STANDUP_START TESTS HERE #########################################
#######################################################################

@setup_data(user_num=2, channel_num=1)
def test_standup_start(users, channels):
    user1 = users[0]
    channel = channels[0]

    # this test should pass with no issue, to assert just check that the time
    # it returns is within some small range
    dev_time = 5

    predicted_finish_time = datetime.now() + timedelta(seconds=dev_time)
    finish_time = standup_start(user1["token"], channel["channel_id"],
                                dev_time)

    assert (predicted_finish_time -
            datetime.fromtimestamp(finish_time["time_finish"])) <= timedelta(6)
    
    # try to start a new standup while this one is active
    pytest.raises(Value_Error, standup_start, user1["token"],
                  channel["channel_id"], dev_time)
    # returns a Value_Error if the channel doesn't exist
    pytest.raises(Value_Error, standup_start, user1["token"],
                  "not_a_real_channel", dev_time)

    # returns an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_start, users[1]["token"],
                  channels[0]["channel_id"], dev_time)

#######################################################################
###  STANDUP_SEND TESTS HERE ##########################################
#######################################################################
@setup_data(user_num=2, channel_num=1)
def test_standup_send(users, channels):
    dev_time = 5

    user1 = users[0]
    channel = channels[0]

    predicted_finish = datetime.now() + timedelta(seconds=dev_time + 1)

    # start the standup
    threading.Thread(target=standup_start, args=(user1["token"],
                                                 channel["channel_id"],
                                                 dev_time)).start()

    # this test should pass with no issue
    assert standup_send(user1["token"], channel["channel_id"], "message") == {}

    # raises a Value_Error if channel does not exist
    pytest.raises(Value_Error, standup_send, user1["token"],
                  "not_a_real_channel", "message")

    # raises an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_send, users[1]["token"],
                  channels[0]["channel_id"], "message")

    # raises a Value_Error if the message is too long
    pytest.raises(Value_Error, standup_send, user1["token"],
                  channel["channel_id"], "a" * 1001)

    # if standup time has stopped
    while datetime.now() <= predicted_finish:
        continue

    pytest.raises(AccessError, standup_send, user1["token"],
                  channel["channel_id"], "message")

#######################################################################
###  STANDUP_ACTIVE TESTS HERE ########################################
#######################################################################
@setup_data(user_num=1, channel_num=1)
def test_standup_active(users, channels):

    dev_time = 5

    user1 = users[0]
    channel = channels[0]

    predicted_finish = datetime.now() + timedelta(seconds=dev_time + 1)

    # start the standup
    threading.Thread(target=standup_start, args=(user1["token"],
                                                 channel["channel_id"],
                                                 dev_time)).start()

    # this test should pass with no issue
    new_standup = standup_active(user1["token"], channel["channel_id"])

    assert new_standup["is_active"]
    assert (datetime.fromtimestamp(new_standup["time_finish"])
            - predicted_finish) <= timedelta(seconds=1)

    # raises a Value_Error if channel does not exist
    pytest.raises(Value_Error, standup_active, user1["token"],
                  "not_a_real_channel")

    # if standup time has stopped
    while datetime.now() <= predicted_finish:
        continue

    assert standup_active(user1["token"], channel["channel_id"]) == \
    {"is_active" : False, "time_finish" : None}
