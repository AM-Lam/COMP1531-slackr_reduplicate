import pytest
from .standup_start import standup_start
from .channels_create import channels_create
from .access_error import *
from .auth_register import auth_register
from .database import *
from datetime import timedelta, datetime


clear_data()


def test_standup_start():
    user = auth_register("valid@email.com", "12345", "John", "Doe")
    #hannel = channels_create(user[token], "Channel 1", False)
    channel = "channel"

    # this test should pass with no issue
    assert standup_start(user["token"], channel) == timedelta(minutes=15)

    # returns a ValueError if the channel doesn't exist
    pytest.raises(ValueError, standup_start, user["token"], "not_a_real_channel")

    # returns an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_start, "badtoken", channel)
