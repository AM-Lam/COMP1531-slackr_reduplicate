import pytest
import jwt
from .database import get_secret
from .access_error import *
from .channel_removeowner import channel_removeowner
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_addowner import channel_addowner


def test_channel_removeowner():
    # boilerplate creation of users and channels
    # user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    # user2 = auth_register("good@email.com", "987654321", "Jen", "Bobs")
    # user3 = auth_register("great@email.com", "00002143", "Jane", "Doe")

    secret = get_secret()
    user1 = {
        "token" : jwt.encode({"u_id" : "111"}, secret, algorithm="HS256"),
        "u_id" : "111"
    }

    user2 = {
        "token" : jwt.encode({"u_id" : "112"}, secret, algorithm="HS256"),
        "u_id" : "112"
    }

    user3 = {
        "token" : jwt.encode({"u_id" : "113"}, secret, algorithm="HS256"),
        "u_id" : "113"
    }
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    channel2 = channels_create(user1["token"], "Channel 2", True)
    
    # now add user2 as an owner to channel1
    channel_addowner(user1["token"], channel1["channel_id"], user2["u_id"])
    
    # test removing user2 as an owner
    assert channel_removeowner(user1["token"], 
                               channel1["channel_id"], user2["u_id"]) == {}
    
    # test removing user2 when they are not an owner
    pytest.raises(ValueError, channel_removeowner, user1["token"], 
                  channel1["channel_id"], user2["u_id"])
    
    # add user2 as an owner to channel1 again
    channel_addowner(user1["token"], channel1["channel_id"], user2["u_id"])
    
    # attempt to remove user2 from channel1 as a user that does not have permis
    # -sions to do so
    pytest.raises(AccessError, channel_removeowner, user3["token"], 
                  channel1["channel_id"], user2["u_id"])
    
    # make user3 an owner of the slackr
    # test removing user2 from channeel1 as a slackr owner, we haven't
    # implemented slackr owners yet so ignore this
    # assert channel_removeowner(user3["token"], 
    #                            channel1["channel_id"], user2["u_id"]) == {}
