import pytest
from .auth import auth_register
from .database import clear_data, get_data
from .channel import channels_create
from .access_error import AccessError, Value_Error


def test_channels_create():
    clear_data()

    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    
    # try to create a valid, public channel
    assert channels_create(user1["token"], "Channel 1", True) == {"channel_id" : 0}

    # try to create a valid, private channel
    assert channels_create(user1["token"], "Channel 1", True) == {"channel_id" : 1}
    
    # try to create a channel with an invalid name
    pytest.raises(Value_Error, channels_create, user1["token"], 
                  "123456789012345678901", False)

