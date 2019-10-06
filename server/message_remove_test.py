import pytest
from channels_leave import channels_leave

def test_message_remove():
    # assert message_remove(token, message_id) == None

    # sender remove the message 
    assert message_remove('person1', 1) == None
    assert message_remove('person2', 3) == None

    #admin remove the message
    assert message_remove('admin1', 5) == None

    # Message is not existed
    with pytest.raises(ValueError):
        message_remove('owner', 45)
        message_remove('person1', 123)

    # Message (based on ID) no longer exists
    def test_message_no_longer_exist():
        # remove the message first
        message_send('person1', 1, 'a')
        message_remove('person1', 1)
        # Now the message is no longer exists
        with pytest.raises(ValueError):
            message_remove('person1', 1)

    # AccessError: 
    # if user is not a member of a certain channel anymore
    def test_error_leave_channel():
        channel_leave('person1', 1)
        with pytest.raises(AccessError) :
            message_remove('person1', 1)

    # Admin of channel A is not channel B but they try to delete message in channel B
    with pytest.raises(AccessError): 
        message_remove('admin1', 2)
        message_remove('admin2', 3)

    # admin of other channel but not even a member in channel_id
    with pytest.raises(AccessError):
        message_remove('admin2', 1)
        message_remove('admin1', 3)