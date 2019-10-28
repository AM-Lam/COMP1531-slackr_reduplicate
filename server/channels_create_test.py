import pytest
from .channels_create import channels_create
from .auth_register import auth_register
from .database import clear_data, get_data
from .access_error import *


def verify_channel(channel_obj, correct_data):
    # print(channel_obj.__dict__)
    if channel_obj.__dict__ == correct_data:
        return True
    return False


def test_channels_create():
    clear_data()

    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")

    db = get_data()
    
    # try to create a valid, public channel
    assert channels_create(user1["token"], "Channel 1", True) == {"channel_id" : 1}

    # try to create a valid, private channel
    assert channels_create(user1["token"], "Channel 1", True) == {"channel_id" : 2}
    
    # try to create a channel with an invalid name
    pytest.raises(ValueError, channels_create, user1["token"], 
                  "123456789012345678901", False)

