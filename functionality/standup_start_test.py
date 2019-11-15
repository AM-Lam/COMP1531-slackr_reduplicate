# pylint: disable=C0114
# pylint: disable=C0116


from datetime import timedelta, datetime
import pytest
from .standup_start import standup_start
from .auth import auth_register
from .channel import channels_create
from .database import clear_data
from .access_error import AccessError, Value_Error
from .decorators import setup_data

@setup_data(user_num=2, channel_num=1)
def test_standup_start(users, channels):

    user1 = users[0]
    user2 = users[1]
    channel = channels[0]

    # this test should pass with no issue, to assert just check that the time
    # it returns is within some small range
    dev_time = 5

    predicted_finish_time = datetime.now() + timedelta(seconds=dev_time)
    finish_time = standup_start(user1["token"], channel["channel_id"])

    assert predicted_finish_time - finish_time <= timedelta(6)

    # returns a Value_Error if the channel doesn't exist
    pytest.raises(Value_Error, standup_start, user1["token"], "not_a_real_channel")

    # returns an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_start, user2["token"], channel["channel_id"])
