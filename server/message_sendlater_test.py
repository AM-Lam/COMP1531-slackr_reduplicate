import pytest
from datetime import datetime, timedelta
from message_sendlater import message_sendlater
from auth_register import auth_register
from channels_create import channels_create
from channel_messages import channel_messages


def test_message_sendlater():
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    channel1 = channels_create(user1["token"], "Channel 1", True)
    
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
    time_sent = datetime.now() + timedelta(minutes=1)
    assert message_sendlate(user1["token"], channel1["channel_id"], "Message",
                            time_sent) == {}
    
    # to test that the message went through check the messages in the channel,
    # to ensure that it isn't actually displayed until the time we specified we
    # will likely have to rely upon observation to an extent
    channel1_msgs = channel_messages(user1["token"], channel1["channel_id"], 0)
    assert channel1_msgs["messages"][0]["message"] == "Message"
    assert channel1_msgs["messages"][0]["time_created"] == time_sent     
    
