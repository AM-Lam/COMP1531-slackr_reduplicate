import pytest
from auth_register import auth_register
from channels_create import channels_create
from channels_listall import channels_listall


def test_channels_listall():
    # create some users and channels for testing
    user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")
    user2 = auth_register("good@email.com", "4321", "Jone", "Bobs")
    
    # ensure that if there are no channels that none are shown
    assert channels_listall(user1["token"]) == {"channels" : [{}]}
    
    channel1 = channels_create(user1["token"], "Channel 1", False)
    
    # ensure that channels_listall shows channels you belong to
    assert channels_list(user1["token"]) == {"channels" : [
        {
            "id" : channel1["id"],
            "name" : channel1["name"]
        }
    ]}
    
    # ensure that channels_listall shows channels you do not belong to
    assert channels_list(user2["token"]) == {"channels" : [
        {
            "id" : channel1["id"],
            "name" : channel1["name"]
        }
    ]}
    
    # create a new channel and repeat the above tests to make sure that multiple
    # channels are listed
    channel2 = channels_create(user1["token"], "Channel 2", False)
    
    assert channels_list(user1["token"]) == {"channels" : [
        {
            "id" : channel1["id"],
            "name" : channel1["name"]
        },
        {
            "id" : channel2["id"],
            "name" : channel2["name"]
        }
    ]}
    
    assert channels_list(user2["token"]) == {"channels" : [
        {
            "id" : channel1["id"],
            "name" : channel1["name"]
        },
        {
            "id" : channel2["id"],
            "name" : channel2["name"]
        }
    ]}
    
    
    # ensure that channels_listall shows private channels you belong to
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
        }
    ]}
    
    # ensure that channels_listall shows private channels that you do not belong
    # to
    
    assert channels_list(user2["token"]) == {"channels" : [
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
        }
    ]}
    
    # seems to be all the testing I can think of right now, might return to this
    # if I can think of more tests

