import pytest
import jwt
from .access_error import *
from .access_error import AccessError
from .channel_addowner import channel_addowner
from .auth_register import auth_register
from .channels_create import channels_create
from .database import get_secret


def test_channel_addowner():
    # boilerplate setting up of users and channels, commented until
    # auth_register working
    # user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    # user2 = auth_register("good@email.com", "987654321", "Jone", "Bobs")
    # user3 = auth_register("amazing@email.com", "00002143", "John", "Boo")

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
    
    # first add a user as an owner to a channel we own
    assert channel_addowner(user1["token"], channel1["channel_id"], 
                            user2["u_id"]) == {}
    
    # now ensure that we can add a user to a channel as an owner after we have
    # been added to it as an owner ourselves (ensure the adding is actually
    # working properly)
    assert channel_addowner(user2["token"], channel1["channel_id"], 
                            user3["u_id"]) == {}
    
    # try to add a user as an owner to a channel they are already an owner
    # on
    pytest.raises(ValueError, channel_addowner, user1["token"],
                  channel1["channel_id"], user2["u_id"])
    
    # try to add a user as an owner to a channel we do not own
    pytest.raises(AccessError, channel_addowner, user2["token"], 
                  channel2["channel_id"], user3["u_id"])
    
    
    # try to add a user as an owner to a channel we do not own, as a slackr 
    # owner
    
    # somehow make user2 an owner of the slackr, commented until we add global
    # admins
    # assert channel_addowner(user2["token"], channel2["channel_id"], 
    #                         user3["u_id"]) == {}

