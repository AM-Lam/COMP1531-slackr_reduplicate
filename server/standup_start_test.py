from datetime import timedelta, datetime
import pytest
from .standup_start import standup_start
from .auth import auth_register
from .channel import channels_create
from .database import *
from .access_error import *



def test_standup_start():
    clear_data()
    
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "1234567890", "John", "Boe")
    channel = channels_create(user["token"], "Channel 1", False)

    # this test should pass with no issue, to assert just check that the time
    # it returns is within some small range
    dev_time = 5
    predicted_finish_time = datetime.now() + timedelta(seconds=dev_time)
    assert (predicted_finish_time - standup_start(user["token"], channel["channel_id"]) <= timedelta(6))

    # returns a ValueError if the channel doesn't exist
    pytest.raises(ValueError, standup_start, user["token"], "not_a_real_channel")

    # returns an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_start, user2["token"], channel["channel_id"])
