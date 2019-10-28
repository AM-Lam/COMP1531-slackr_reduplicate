import pytest
from .channel import channels_create, channels_list, channel_join, channel_leave
from .auth_register import auth_register
from .database import *


def test_channels_list():
    clear_data()

    # boilerplate user/channel creation code
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    user2 = auth_register("new@email.com", "987654321", "Doug", "Jones")
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    
    # try to see the channels of a user with no channels
    assert channels_list(user2["token"]) == {"channels" : []}
    
    # try to see the channels of a user that owns one public channel
    assert channels_list(user1["token"]) == { "channels" : [{
        "channel_id" : channel1["channel_id"],
        "name" : "Channel 1"
    }]}
    
    # add user2 to channel1 and check that we can list it as belonging to that
    # channel
    channel_join(user2["token"], channel1["channel_id"])
    assert channels_list(user2["token"]) == { "channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        }
    ]}
    
    # create a new channel, test that multiple channels are shown
    channel2 = channels_create(user1["token"], "Channel 2", True)
    assert channels_list(user1["token"]) == { "channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        },
    ]}
    
    # create a private channel, test that it is shown in the list
    channel3 = channels_create(user1["token"], "Channel 3", False)
    assert channels_list(user1["token"]) == { "channels" : [
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
        },
    ]}
    
    # test that if a channel only has one channel, and it is private, that it
    # is shown in the list
    channel_leave(user1["token"], channel1["channel_id"])
    channel_leave(user1["token"], channel2["channel_id"])
    assert channels_list(user1["token"]) == { "channels" : [
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        }
    ]}
    
    
    
