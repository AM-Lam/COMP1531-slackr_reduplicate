import pytest
import channel_leave


def test_channel_leave():
    # first check the simplest case, if the user can leave a channel they are in
    assert channel_leave.channel_leave(1, 1) == None

    # now check that attempting to leave a non-existent channel raises an exception
    pytest.raises(ValueError, channel_leave.channel_leave, 1, 10)
