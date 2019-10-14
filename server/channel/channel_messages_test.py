import channel_messages
import channels_create
import pytest
import auth_register
import channel_invite
import message_send


#############################################################################################################################################
# channel does not exist
def test_channel_exists_or_not():
    with pytest.raises(ValueError, match=r"*"):
        channel_messages.does_channel_exist(invalidchannelid)

############################################################################################################################################
# start greater than the total number of messages
def test_is_start_too_big():
    user1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register.auth_register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
    user3 = auth_register.auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
    token1 = user1['token']
    token2 = user2['token']
    token3 = user3['token']
    uid1 = user1['u_id']
    uid2 = user2['u_id']
    uid3 = user3['u_id']
    # user1 will be the channel owner
    unswchannel = channels_create.channels_create(token1, unswchannel, True)
    unswchannelid = unswchannel['channel_id']
    # adding user 2 and 3 to the channel
    channel_invite.channel_invite(token2, unswchannelid, uid2)
    channel_invite.channel_invite(token3, unswchannelid, uid3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send.message_send(token1, unswchannelid, messageloop)
    # now lets call channel messages...
    with pytest.raises(ValueError, match=r"*"):
        channel_messages.channel_messages(token1, unswchannelid, 93)

############################################################################################################################################
# INVALID USER
def test_is_start_too_big():
    user1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register.register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
    user3 = auth_register.auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
    token1 = user1['token']
    token2 = user2['token']
    token3 = user3['token']
    uid1 = user1['u_id']
    uid2 = user2['u_id']
    uid3 = user3['u_id']
    # user1 will be the channel owner
    usydchannel = channels_create.channels_create(token1, usydchannel, True)
    usydchannelid = usydchannel['channel_id']
    # adding  ONLY user 2 to the channel
    channel_invite.channel_invite(token2, usydchannelid, uid2)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send.message_send(token1, usydchannelid, messageloop)
    # now lets call channel messages...
    with pytest.raises(AccessError, match=r"*"):
        channel_messages.channel_messages(token3, usydchannelid, 2)

###########################################################################################################################################
# start greater than the total number of messages
def test_is_start_too_big():
    user1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register.register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
    user3 = auth_register.auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
    token1 = user1['token']
    token2 = user2['token']
    token3 = user3['token']
    uid1 = user1['u_id']
    uid2 = user2['u_id']
    uid3 = user3['u_id']
    # user1 will be the channel owner
    utschannel = channels_create.channels_create(token1, utschannel, True)
    utschannelid = utschannel['channel_id']
    # adding user 2 and 3 to the channel
    channel_invite.channel_invite(token2, utschannelid, uid2)
    channel_invite.channel_invite(token3, utschannelid, uid3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send.message_send(token1, utschannelid, messageloop)
    # now lets call channel messages...
    with pytest.raises(ValueError, match=r"*"):
        channel_messages.channel_messages(token1, utschannelid, 93)

###########################################################################################################################################
# END SHOULD BE -1 AS THE LEAST RECENT MESSAGE WAS SENT OUT.....
def test_is_start_too_big():
    user1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register.register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
    user3 = auth_register.auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
    token1 = user1['token']
    token2 = user2['token']
    token3 = user3['token']
    uid1 = user1['u_id']
    uid2 = user2['u_id']
    uid3 = user3['u_id']
    # user1 will be the channel owner
    yeetchannel = channels_create.channels_create(token1, yeetchannel, True)
    yeetchannelid = yeetchannel['channel_id']
    # adding user 2 and 3 to the channel
    channel_invite.channel_invite(token2, yeetchannelid, uid2)
    channel_invite.channel_invite(token3, yeetchannelid, uid3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send.message_send(token1, yeetchannelid, messageloop)
    # now lets call channel messages...
    mesdict = channel_messages.channel_messages(token1, yeetchannelid, 40)
    assert mesdict['start'] == 40
    assert mesdict['end'] == -1

###########################################################################################################################################
# SOME IN BETWEEN INTERVAL TESTING:::::::::::::::::::::::::::::::::
def test_is_start_too_big():
    user1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register.register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
    user3 = auth_register.auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
    token1 = user1['token']
    token2 = user2['token']
    token3 = user3['token']
    uid1 = user1['u_id']
    uid2 = user2['u_id']
    uid3 = user3['u_id']
    # user1 will be the channel owner
    unichannel = channels_create.channels_create(token1, unichannel, True)
    unichannelid = unichannel['channel_id']
    # adding user 2 and 3 to the channel
    channel_invite.channel_invite(token2, unichannelid, uid2)
    channel_invite.channel_invite(token3, unichannelid, uid3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send.message_send(token1, unichannelid, messageloop)
    # now lets call channel messages...
    mesdict1 = channel_messages.channel_messages(token1, unichannelid, 10)
    assert mesdict1['start'] == 10
    assert mesdict1['end'] == 60

