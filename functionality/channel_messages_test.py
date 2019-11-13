import pytest
from .auth import auth_register
from .message import message_send
from .channel import channel_messages, channels_create, channel_invite
from .access_error import AccessError, Value_Error
from .database import clear_data


def test_run_all():
    clear_data()

    # initialisation
    user1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
    user3 = auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
    
    token1 = user1['token']
    token2 = user2['token']
    token3 = user3['token']
    
    uid1 = user1['u_id']
    uid2 = user2['u_id']
    uid3 = user3['u_id']

    # start greater than the total number of messages
    # user1 will be the channel owner
    unswchannel = channels_create(token1, 'unswchannel', True)
    unswchannelid = unswchannel['channel_id']
    # adding user 2 and 3 to the channel
    channel_invite(token1, unswchannelid, uid2)
    channel_invite(token1, unswchannelid, uid3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token1, unswchannelid, messageloop)
    # now lets call channel messages...
    with pytest.raises(Value_Error, match=r"*"):
        channel_messages(token1, unswchannelid, 93)

    # INVALID USER
    # user1 will be the channel owner
    usydchannel = channels_create(token1, 'usydchannel', True)
    usydchannelid = usydchannel['channel_id']
    # adding  ONLY user 2 to the channel
    channel_invite(token1, usydchannelid, uid2)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token1, usydchannelid, messageloop)
    # now lets call channel messages...
    with pytest.raises(AccessError, match=r"*"):
        channel_messages(token3, usydchannelid, 2)

    # END SHOULD BE -1 AS THE LEAST RECENT MESSAGE WAS SENT OUT
    # user1 will be the channel owner
    yeetchannel = channels_create(token1, 'yeetchannel', True)
    yeetchannelid = yeetchannel['channel_id']
    # adding user 2 and 3 to the channel
    channel_invite(token1, yeetchannelid, uid2)
    channel_invite(token1, yeetchannelid, uid3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token1, yeetchannelid, messageloop)
    # now lets call channel messages...
    mesdict = channel_messages(token1, yeetchannelid, 40)
    assert mesdict['start'] == 40
    assert mesdict['end'] == -1

    # SOME IN BETWEEN INTERVAL TESTING
    # user1 will be the channel owner
    unichannel = channels_create(token1, 'unichannel', True)
    unichannelid = unichannel['channel_id']
    # adding user 2 and 3 to the channel
    channel_invite(token1, unichannelid, uid2)
    channel_invite(token1, unichannelid, uid3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token1, unichannelid, messageloop)
    # now lets call channel messages...
    mesdict1 = channel_messages(token1, unichannelid, 10)
    assert mesdict1['start'] == 10
    assert mesdict1['end'] == 60