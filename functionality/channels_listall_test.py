import pytest
from .auth import auth_register
from .channel import channels_listall, channels_create
from .database import clear_data


def test_channels_listall():
    clear_data()
    
    # create some users and channels for testing, commented for now
    # until auth_register works
    user1 = auth_register("valid@email.com", "0123456789", "Bob", "Jones")
    user2 = auth_register("good@email.com", "9876543210", "Jone", "Bobs")
    
    # ensure that if there are no channels that none are shown
    assert channels_listall(user1["token"]) == {"channels" : []}
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    
    # ensure that channels_listall shows channels you belong to
    assert channels_listall(user1["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        }
    ]}
    
    # ensure that channels_listall shows channels you do not belong to
    assert channels_listall(user2["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        }
    ]}
    
    # create a new channel and repeat the above tests to make sure that multiple
    # channels are listed
    channel2 = channels_create(user1["token"], "Channel 2", True)
    
    assert channels_listall(user1["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        }
    ]}
    
    assert channels_listall(user2["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        }
    ]}
    
    
    # ensure that channels_listall shows private channels you belong to
    channel3 = channels_create(user1["token"], "Channel 3", False)
    
    assert channels_listall(user1["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        },
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        }
    ]}
    
    # ensure that channels_listall shows private channels that you do not belong
    # to
    
    assert channels_listall(user2["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        },
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        }
    ]}
    
    # seems to be all the testing I can think of right now, might return to this
    # if I can think of more tests

