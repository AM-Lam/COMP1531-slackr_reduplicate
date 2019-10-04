import pytest
from channels_list import channels_list
from channels_create import channels_create
from channel_leave import channel_leave
from auth_register import auth_register


def test_channels_list():
    # boilerplate user/channel creation code
    user1 = auth__register("valid@email.com", "1234", "Bob", "Jones")
    user2 = auth_register("new@email.com", "4321", "Doug", "Jones")
    
    channel1 = channels_create(user1["token"], "Channel 1", False)
    
    # try to see the channels of a user with no channels
    assert channels_list(user2["token"]) == {"channels" : []}
    
    # try to see the channels of a user that owns one public channel
    assert channels_list(user1["token"]) == {"channels" : [{
        "id" : channel1["id"],
        "name" : channel1["name"]
    }]}
    
    # add user2 to channel1 and check that we can list it as belonging to that
    # channel
    channel_join(user2["token"], channel1["id"])
    assert channels_list(user2["token"]) == {"channels" : [
        {
            "id" : channel1["token"],
            "name" : channel1["name"]
        }
    ]}
    
    # create a new channel, test that multiple channels are shown
    channel2 = channels_create(user1["token"], "Channel 2", False)
    assert channels_list(user1["token"]) == {"channels" : [
        {
            "id" : channel1["id"],
            "name" : channel1["name"]
        },
        {
            "id" : channel2["id"],
            "name" : channel2["name"]
        },
    ]}
    
    # create a private channel, test that it is shown in the list
    channel3 = channels_create(user1["token"], "Channel 3", True)
    assert channels_list(user1["token"]) == {"channels" : [
        {
            "id" : channel1["id"],
            "name" : channel1["name"]
        },
        {
            "id" : channel2["id"],
            "name" : channel2["name"]
        },
        {
            "id" : channel3["id"],
            "name" : channel3["name"]
        },
    ]}
    
    # test that if a channel only has one channel, and it is private, that it
    # is shown in the list
    channel_leave(user1["token"], channel1["id"])
    channel_leave(user1["token"], channel2["id"])
    assert channels_list(user1["token"]) == {"channels" : [
        {
            "id" : channel3["id"],
            "name" : channel3["name"]
        }
    ]}
    
    
    
