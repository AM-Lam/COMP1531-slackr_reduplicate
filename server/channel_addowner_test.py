import pytest
from access_error import AccessError
from channel_addowner import channel_addowner


def channel_addowner_test():
    # boilerplate setting up of users and channels
    user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")
    user2 = auth_register("good@email.com", "4321", "Jone", "Bobs")
    user3 = auth_register("amazing@email.com", "2143", "John", "Boo")
    
    channel1 = channels_create(user1["token"], "Channel 1", False)
    channel2 = channels_create(user1["token"], "Channel 2", False)
    
    # first add a user as an owner to a channel we own
    assert channel_addowner(user1["token"], channel1["id"], user2["u_id"]) == {}
    
    # now ensure that we can add a user to a channel as an owner after we have
    # been added to it as an owner ourselves (ensure the adding is actually
    # working properly)
    assert channel_addowner(user2["token"], channel1["id"], user3["u_id"]) == {}
    
    # try to add a user as an owner to a channel they are already an owner
    # on
    pytest.raises(ValueError, channel_addowner, user1["token"], channel1["id"],
                  user2["u_id"])
    
    # try to add a user as an owner to a channel we do not own
    pytest.raises(AccessError, channel_addowner, user2["token"], channel2["id"],
                  user3["u_id"])
    
    
    # try to add a user as an owner to a channel we do not own, as a slackr 
    # owner
    
    # somehow make user2 an owner of the slackr
    assert channel_addowner(user2["token"], channel2["id"], user3["u_id"]) == {}

