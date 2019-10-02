import pytest
import channel_leave


def test_channel_leave_pass():
    # first check the simplest case, if the user can leave a channel they are in
    assert channel_leave.channel_leave(1, 1) == None
    assert channel_leave.channel_leave(2, 1) == None

def test_channel_leave_fail():
    # now check that attempting to leave a non-existent channel raises an exception
    pytest.raises(ValueError, channel_leave.channel_leave, 1, 10)

    # try to leave a channel the user is not a part of, this should fail quietely
    assert channel_leave.channel_leave(1, 2) == None
