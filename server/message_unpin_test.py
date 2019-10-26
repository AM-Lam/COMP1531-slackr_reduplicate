import pytest
from .access_error import *
from .channel_leave import channel_leave
from .message_unpin import message_unpin

    
def test_message_unpin():
    #assert message_unpin(token, message_id) == None
    assert message_unpin('admin1', 1) == None
    assert message_unpin('owner', 5) == None

    def test_basic_case():
        message_pin('owner', 3)
        message_unpin('owner', 3)
    
    with pytest.raises(ValueError):
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_unpin('admin1', 78)
    #  The authorised user is not an admin
        message_unpin('person1', 1)
        message_unpin('person2', 3)
        message_unpin('person3', 1)
        message_unpin('person3', 2)

    #  Message with ID message_id is already unpinned
    def double_unpin():
        message_pin('admin2', 1)
        message_unpin('admin2', 1)
        with pytest.raises(ValueError):
            message_unpin('admin2', 1)

    #  The authorised user is not a member of the channel that the message is within
    def test_error_leave_channel():
        message_pin('admin1', 1)
        channel_leave('admin1', 1)
        with pytest.raises(AccessError) :
            message_unpin('admin1', 1)
    
