import jwt
import pytest
from datetime import datetime, timedelta
from .database import get_data, clear_data
from .message_sendlater import message_sendlater
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_messages import channel_messages
from .access_error import *


def test_message_sendlater():
    clear_data()
    
    server_data = get_data()
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    
    # create the channel we test with
    channel1 = channels_create(user1["token"], "Channel 1", True)

    # get the channel object, we need this to check if messages were sent
    channelObj = server_data["channels"][0]
    
    # first test some cases that should raise exceptions
    # message > 1000 characters
    pytest.raises(ValueError, message_sendlater, user1["token"], 
                  channel1["channel_id"], "X" * 1001, 
                  datetime.now() + timedelta(minutes=1))
    
    # time sent is in the past
    pytest.raises(ValueError, message_sendlater, user1["token"], 
                  channel1["channel_id"], "Message", datetime(2000, 1, 1))
    
    # non-existent channel
    pytest.raises(ValueError, message_sendlater, user1["token"], 
                  404, "Message", datetime.now() + timedelta(minutes=1))
    
    # now try to send a valid message in the future
    time_sent = datetime.utcnow() + timedelta(seconds=5)
    assert message_sendlater(user1["token"], channel1["channel_id"], "Message",
                            time_sent) == { "message_id" : 1 }

    # ensure that the message has not yet appeared
    assert len(channelObj.get_messages()) == 0

    
    # wait until the time has passed then check if the message was sent
    # (wait a little longer just to ensure that we aren't checking for the
    # message at the same time as it is sent)
    while datetime.utcnow() < time_sent + timedelta(seconds=1):
        continue
    
    assert len(channelObj.get_messages()) == 1
