import pytest
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .access_error import *
from .database import *


def test_channel_join():
    clear_data()

    # commented until auth_register working
    user1 = auth_register("valid@email.com", "strong-password", "John", "Doe")
    user2 = auth_register("good@email.com", "another-password", "Jack", "Doe")
    
    channel1 = channels_create(user1['token'], "Channel 1", True)
    channel2 = channels_create(user1['token'], "Channel 2", False)
    
    # first try to join a public server that exists
    assert channel_join(user2['token'], channel1['channel_id']) == {}
    
    # now try to join a server that does not exist, this should fail with an
    # access error
    pytest.raises(ValueError, channel_join, user2['token'], 404)
    
    # try to join a server that exists, but is private as a regular user
    pytest.raises(AccessError, channel_join, user2['token'], 
                  channel2['channel_id'])
    
    # try to join a server that exists, but is private as an admin
    # first we'll have to make the second user an admin, not sure how this will
    # work yet
    pytest.raises(AccessError, channel_join, user2['token'], 
                  channel2['channel_id'])
