import pytest
from channels_create import channels_create
from auth_register import auth_register


def test_channels_create():
    user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")
    
    # try to create a valid, public channel
    channel1 = channels_create(user1["token"], "Channel 1", True)
    assert channel1 is not None
    
    # try to create a valid, private channel
    channel1 = channels_create(user1["token"], "Channel 1", False)
    assert channel1 is not None
    
    # try to create a channel with an invalid name
    pytest.raises(ValueError, channels_create, user1["token"], 
                  "123456789012345678901", False)

