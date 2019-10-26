import pytest
from .access_error import *
from .message_pin import message_pin
from .channel_leave import channel_leave

def test_message_pin():
    # assert message_pin(token, message_id) == None
    assert message_pin('admin1', 1) == None
    assert message_pin('admin1', 5) == None
    assert message_pin('admin2', 2) == None
    assert message_pin('owner', 3) == None
    assert message_pin('owner', 4) == None

    with pytest.raises(ValueError):
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_pin('admin1', 456)

    #  The authorised user is not an admin
        message_pin('admin1', 3)
        message_pin('admin1', 4)
        message_pin('admin2', 1)

    #  Message with ID message_id is already pinned
    def double_pin():
        message_pin('admin2', 2)
        with pytest.raises(ValueError):
            message_pin('admin2', 2)

    #  The authorised user is not a member of the channel that the message is within
    def test_error_leave_channel():
        channel_leave('admin2', 3)
        with pytest.raises(AccessError):
            message_pin('admin2', 2)
    
