import pytest
import threading
from .standup_send import standup_send
from .standup_start import standup_start
from .channels_create import channels_create
from .access_error import *
from .auth_register import auth_register
from .database import *
from datetime import timedelta, datetime


def test_standup_send():

    clear_data()

    dev_time = 5

    user = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "John", "Zoe")

    channel = channels_create(user["token"], "Channel 1", False)

    predicted_finish = datetime.now() + timedelta(seconds=dev_time + 1)

    # start the standup
    threading.Thread(target=standup_start, args=(user["token"], channel["channel_id"])).start()

    # this test should pass with no issue
    assert standup_send(user["token"], channel["channel_id"], "message") == None

    # raises a ValueError if channel does not exist
    pytest.raises(ValueError, standup_send, user["token"], "not_a_real_channel", "message")

    # raises an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_send, user2["token"], channel["channel_id"], "message")

    # raises a ValueError if the message is too long
    pytest.raises(ValueError, standup_send, user["token"], channel["channel_id"], "a" * 1001)
    
    # if standup time has stopped
    while datetime.now() <= predicted_finish:
        continue

    pytest.raises(AccessError, standup_send, user["token"], channel["channel_id"], "message")
