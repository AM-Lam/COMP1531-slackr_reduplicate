# pylint: disable=C0114
# pylint: disable=C0116


import threading
from datetime import timedelta, datetime
import pytest
from .standup_send import standup_send
from .standup_start import standup_start
from .auth import auth_register
from .database import clear_data
from .channel import channels_create
from .access_error import AccessError, Value_Error
from .decorators import setup_data

@setup_data(user_num=2, channel_num=1)
def test_standup_send(users, channels):

    dev_time = 5

    user1 = users[0]
    user2 = users[1]
    channel = channels[0]

    predicted_finish = datetime.now() + timedelta(seconds=dev_time + 1)

    # start the standup
    threading.Thread(target=standup_start, args=(user1["token"], channel["channel_id"])).start()

    # this test should pass with no issue
    assert standup_send(user1["token"], channel["channel_id"], "message") is None

    # raises a Value_Error if channel does not exist
    pytest.raises(Value_Error, standup_send, user1["token"], "not_a_real_channel", "message")

    # raises an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_send, user2["token"], channel["channel_id"], "message")

    # raises a Value_Error if the message is too long
    pytest.raises(Value_Error, standup_send, user1["token"], channel["channel_id"], "a" * 1001)

    # if standup time has stopped
    while datetime.now() <= predicted_finish:
        continue

    pytest.raises(AccessError, standup_send, user1["token"], channel["channel_id"], "message")
