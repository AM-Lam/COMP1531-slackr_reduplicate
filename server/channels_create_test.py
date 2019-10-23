import pytest
from .channels_create import channels_create
from .auth_register import auth_register
from .database import *


def verify_channel(channel_obj, correct_data):
    # print(channel_obj.__dict__)
    if channel_obj.__dict__ == correct_data:
        return True
    return False


def test_channels_create():
    # comment this out until we can ensure that auth_register is working
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    user1 = {
        "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTExIn0.dyT88tdeqRfTRsfjQRenygNT_ywC-wTAFWlvMUHfhxI"
    }

    db = get_data()
    
    # try to create a valid, public channel
    channel1 = channels_create(user1["token"], "Channel 1", True)
    
    # check that the channel exists
    assert channel1 is not None

    # check that the database was correctly updated
    assert verify_channel(db["channels"][0], 
                         {
                            "_channel_id" : 1,
                            "_channel_name" : "Channel 1",
                            "_messages" : [],
                            "_members" : ["111"],
                            "_public" : True
                         }
                         )
    
    # reset channel1
    channel1 = None

    # try to create a valid, private channel
    channel1 = channels_create(user1["token"], "Channel 1", False)
    assert channel1 is not None

    # check that the database was correctly updated
    assert verify_channel(db["channels"][1], 
                         {
                            "_channel_id" : 2,
                            "_channel_name" : "Channel 1",
                            "_messages" : [],
                            "_members" : ["111"],
                            "_public" : False
                         }
                         )
    
    # try to create a channel with an invalid name
    pytest.raises(ValueError, channels_create, user1["token"], 
                  "123456789012345678901", False)

