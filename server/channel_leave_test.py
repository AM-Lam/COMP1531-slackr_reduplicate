from auth_register import auth_register
from channels_create import channels_create
import pytest
import channel_leave


def test_channel_leave():
    # boilerplate user and channel creation stuff
    user1 = auth_register("valid@email.com", "verystrong", "John", "Doe")
    channel1 = channels_create(user1["token"], "New Channel", False)

    # first check the simplest case, if the user can leave a channel they are in
    assert channel_leave.channel_leave(user1["token"], channel1["id"]) == {}

    # now check that attempting to leave a non-existent channel raises an 
    # exception
    pytest.raises(ValueError, channel_leave.channel_leave, 
                  user1["token"], "fake_id")

    # try to leave a channel the user is not a part of - this should fail 
    # quietely (see assumptions.md)
    assert channel_leave.channel_leave(user1["token"], "fake_id") == {}

