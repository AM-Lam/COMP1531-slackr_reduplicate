import pytest
from .channel_leave import channel_leave
from .auth_register import auth_register
from .channels_create import channels_create



def test_channel_leave():
    # boilerplate user and channel creation stuff, comment out until
    # auth_register is working
    user1 = auth_register("valid@email.com", "verystrong", "John", "Doe")
    
    channel1 = channels_create(user1["token"], "New Channel", True)
    channel2 = channels_create(user1["token"], "A New Channel", False)
    channel3 = channels_create(user1["token"], "Good 'Ol Channel", True)

    # first check the simplest case, if the user can leave a channel they are in
    assert channel_leave(user1["token"], channel1["channel_id"]) == {}

    # now try to leave a private channel
    assert channel_leave(user1["token"], channel2["channel_id"]) == {}

    # now check that attempting to leave a non-existent channel raises an 
    # exception
    pytest.raises(ValueError, channel_leave, user1["token"], 404)

    # try to leave a channel the user is not a part of - this should fail 
    # quietely (see assumptions.md)
    assert channel_leave(user1["token"], channel3["channel_id"]) == {}

