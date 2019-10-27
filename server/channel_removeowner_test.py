import pytest
import jwt
from .database import clear_data, get_data
from .channel_removeowner import channel_removeowner
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_addowner import channel_addowner
from .access_error import *


def test_channel_removeowner():
    clear_data()

    server_data = get_data()

    # boilerplate creation of users and channels
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    user2 = auth_register("good@email.com", "987654321", "Jen", "Bobs")
    user3 = auth_register("great@email.com", "00002143", "Jane", "Doe")

    user3_obj = None
    for u in server_data["users"]:
        if u.get_u_id() == user3["u_id"]:
            user3_obj = u
            break
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    channel2 = channels_create(user1["token"], "Channel 2", True)
    
    # now add user2 as an owner to channel1
    channel_addowner(user1["token"], channel1["channel_id"], user2["u_id"])
    
    # test removing user2 as an owner
    assert channel_removeowner(user1["token"], channel1["channel_id"],
                               user2["u_id"]) == {}
    
    # test removing user2 when they are not an owner
    pytest.raises(ValueError, channel_removeowner, user1["token"],
                  channel1["channel_id"], user2["u_id"])
    
    # add user2 as an owner to channel1 again
    channel_addowner(user1["token"], channel1["channel_id"], user2["u_id"])
    
    # attempt to remove user2 from channel1 as a user that does not have permis
    # -sions to do so
    pytest.raises(AccessError, channel_removeowner, user3["token"], 
                  channel1["channel_id"], user2["u_id"])
    
    # test removing user2 from channeel1 as a slackr owner
    user3_obj.set_global_admin(True)
    assert channel_removeowner(user3["token"], channel1["channel_id"],
                               user2["u_id"]) == {}
    
    # try to remove an owner from a channel that does not exist
    pytest.raises(ValueError, channel_removeowner, user1["token"], 128,
                  user2["u_id"])