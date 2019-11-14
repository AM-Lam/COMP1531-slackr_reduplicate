import pytest
import jwt
from .auth import auth_register
from .message import message_send
from .channel import channels_create, channel_addowner, channel_join, channel_details, channel_invite, channel_leave, channel_messages, channel_removeowner, channels_list, channels_listall
from .database import *
from .access_error import AccessError, Value_Error


#######################################################################
###  CHANNEL_ADDOWNER TESTS HERE ######################################
#######################################################################

def test_channel_addowner():
    clear_data()
    
    # boilerplate setting up of users and channels, commented until
    # auth_register working
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    user2 = auth_register("good@email.com", "987654321", "Jone", "Bobs")
    user3 = auth_register("amazing@email.com", "00002143", "John", "Boo")
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    channel2 = channels_create(user1["token"], "Channel 2", True)
    
    # first add a user as an owner to a channel we own
    assert channel_addowner(user1["token"], channel1["channel_id"], user2["u_id"]) == {}
    
    # now ensure that we can add a user to a channel as an owner after we have
    # been added to it as an owner ourselves (ensure the adding is actually
    # working properly)
    assert channel_addowner(user2["token"], channel1["channel_id"], user3["u_id"]) == {}
    
    # try to add a user as an owner to a channel they are already an owner
    # on
    pytest.raises(Value_Error, channel_addowner, user1["token"], channel1["channel_id"], user2["u_id"])
    
    # try to add a user as an owner to a channel we do not own
    pytest.raises(AccessError, channel_addowner, user2["token"], channel2["channel_id"], user3["u_id"])
    
    
    # try to add a user as an owner to a channel we do not own, as a slackr 
    # owner
    
    # somehow make user2 an owner of the slackr, commented until we add global
    # admins
    # assert channel_addowner(user2["token"], channel2["channel_id"], 
    #                         user3["u_id"]) == {}


#######################################################################
###  CHANNEL_DETAILS TESTS HERE #######################################
#######################################################################

def test_channel_details():
    clear_data()

    #initialisation
    user1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
    user3 = auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
    
    token1 = user1['token']
    token2 = user2['token']
    
    
    # user1 will be the channel owner
    unswchannel = channels_create(token1, 'unswchannel', True)
    unswchannelid = unswchannel['channel_id']


    # what if the channel does not exist?
    invalid_channel = 999
    with pytest.raises(Value_Error , match=r"*"):
        get_channel(invalid_channel)

    # user2 is not a part of the channel
    assert is_user_member(user2["u_id"], unswchannel["channel_id"]) == False

    # adding user 2 to the channel
    channel_join(user2["token"], unswchannelid)
    
    # search details
    detaildict = channel_details(token2, unswchannelid)
    assert detaildict['name'] == "unswchannel"
    assert detaildict['owner_members'] == [
        {'u_id': 1, 'name_first': 'user', 'name_last': 'a'}]
    
    assert detaildict['all_members'] == [
        {'u_id': 1, 'name_first': 'user', 'name_last': 'a'},
        {'u_id': 2, 'name_first': 'ussr', 'name_last': 'b'}]
    
    # add user 3
    channel_join(user3["token"], unswchannelid)
    
    # search details
    detaildict2 = channel_details(token2, unswchannelid)
    assert detaildict2['name'] == "unswchannel"
    
    assert detaildict2['owner_members'] == [
        {'u_id': 1, 'name_first': 'user', 'name_last': 'a'}]
    
    assert detaildict2['all_members'] == [
        {'u_id': 1, 'name_first': 'user', 'name_last': 'a'},
        {'u_id': 2, 'name_first': 'ussr', 'name_last': 'b'},
        {'u_id': 3, 'name_first': 'the', 'name_last': 'rabbit'}]


#######################################################################
###  CHANNEL_INVITE TESTS HERE ########################################
#######################################################################

def test_channel_invite():
    clear_data()
    
    # first we create two users:
    user1 = auth_register('user1@domain.com' , '1234567890', 'user' , 'a')
    user2 = auth_register('user2@domain.com' , '0987654321', 'ussr' , 'b')
    
    token1 = user1['token']
    token2 = user2['token']
    
    uid1 = user1['u_id']
    uid2 = user2['u_id']

    # lets create an invalid non existant user id
    uidfaux = 999999999999999999999999999999999999999999999999999999999999999999

    # now we create a channel
    unswchannel = channels_create(token1, "unswchannel", True)
    unswchannelid = unswchannel['channel_id']
    # user1 is now a part of unswchannel

    # test if the user is valid.
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite('3131313133', unswchannelid, uid2)

    # test if user does not exist on application database
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token1, unswchannelid, 'jl mackie')

    # user exists but is already a part of that channel then invite should raise Value_Error
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token1, unswchannelid, uid1)

    # what if the channel does not exist?
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token1, "this channel does not exist", uid2)

    # add user 2 to the channel (invitee -> user 1)
    channel_invite(token1, unswchannelid, uid2)
    # user 2 is already a part of that channel the invite should raise Value_Error
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token1, unswchannelid, uid2)


#######################################################################
###  CHANNEL_JOIN TESTS HERE ##########################################
#######################################################################

def test_channel_join():
    clear_data()

    # commented until auth_register working
    user1 = auth_register("valid@email.com", "strong-password", "John", "Doe")
    user2 = auth_register("good@email.com", "another-password", "Jack", "Doe")
    
    channel1 = channels_create(user1['token'], "Channel 1", True)
    channel2 = channels_create(user1['token'], "Channel 2", False)
    
    # first try to join a public server that exists
    assert channel_join(user2['token'], channel1['channel_id']) == {}
    
    # now try to join a server that does not exist, this should fail with an
    # access error
    pytest.raises(Value_Error, channel_join, user2['token'], 404)
    
    # try to join a server that exists, but is private as a regular user
    pytest.raises(AccessError, channel_join, user2['token'], 
                  channel2['channel_id'])
    
    # try to join a server that exists, but is private as an admin
    # first we'll have to make the second user an admin, not sure how this will
    # work yet
    pytest.raises(AccessError, channel_join, user2['token'], 
                  channel2['channel_id'])


#######################################################################
###  CHANNEL_LEAVE TESTS HERE #########################################
#######################################################################

def test_channel_leave():
    clear_data()

    # boilerplate user and channel creation stuff, comment out until
    # auth_register is working
    user1 = auth_register("valid@email.com", "verystrong", "John", "Doe")
    
    channel1 = channels_create(user1["token"], "New Channel", True)
    channel2 = channels_create(user1["token"], "A New Channel", False)
    channel3 = channels_create(user1["token"], "Good 'Ol Channel", True)

    # first check the simplest case, if the user can leave a channel they are in
    assert channel_leave(user1["token"], channel1["channel_id"]) == {}

    # now try to leave a private channel
    assert channel_leave(user1["token"], channel2["channel_id"]) == {}

    # now check that attempting to leave a non-existent channel raises an 
    # exception
    pytest.raises(Value_Error, channel_leave, user1["token"], 404)

    # try to leave a channel the user is not a part of - this should fail 
    # quietely (see assumptions.md)
    assert channel_leave(user1["token"], channel3["channel_id"]) == {}


#######################################################################
###  CHANNEL_MESSAGES TESTS HERE ######################################
#######################################################################

def test_channel_messages():
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


#######################################################################
###  CHANNEL_REMOVEOWNER TESTS HERE ###################################
#######################################################################

def test_channel_removeowner():
    clear_data()

    server_data = get_data()

    # boilerplate creation of users and channels
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    user2 = auth_register("good@email.com", "987654321", "Jen", "Bobs")
    user3 = auth_register("great@email.com", "00002143", "Jane", "Doe")

    user3_obj = get_user(user3["u_id"])
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    
    # now add user2 as an owner to channel1
    channel_addowner(user1["token"], channel1["channel_id"], user2["u_id"])
    
    # test removing user2 as an owner
    assert channel_removeowner(user1["token"], channel1["channel_id"],
                               user2["u_id"]) == {}
    
    # test removing user2 when they are not an owner
    pytest.raises(Value_Error, channel_removeowner, user1["token"],
                  channel1["channel_id"], user2["u_id"])
    
    # add user2 as an owner to channel1 again
    channel_addowner(user1["token"], channel1["channel_id"], user2["u_id"])
    
    # attempt to remove user2 from channel1 as a user that does not have permis
    # -sions to do so
    pytest.raises(AccessError, channel_removeowner, user3["token"], 
                  channel1["channel_id"], user2["u_id"])
    
    # test removing user2 from channel1 as a slackr owner
    user3_obj.set_global_admin(True)
    assert channel_removeowner(user3["token"], channel1["channel_id"],
                               user2["u_id"]) == {}
    
    # try to remove an owner from a channel that does not exist
    pytest.raises(Value_Error, channel_removeowner, user1["token"], 128,
                  user2["u_id"])


#######################################################################
###  CHANNEL_CREATE TESTS HERE ########################################
#######################################################################

def test_channels_create():
    clear_data()

    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    
    # try to create a valid, public channel
    assert channels_create(user1["token"], "Channel 1", True) == {"channel_id" : 1}

    # try to create a valid, private channel
    assert channels_create(user1["token"], "Channel 1", True) == {"channel_id" : 2}
    
    # try to create a channel with an invalid name
    pytest.raises(Value_Error, channels_create, user1["token"], 
                  "123456789012345678901", False)


#######################################################################
###  CHANNEL_LIST TESTS HERE ##########################################
#######################################################################

def test_channels_list():
    clear_data()

    # boilerplate user/channel creation code
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    user2 = auth_register("new@email.com", "987654321", "Doug", "Jones")
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    
    # try to see the channels of a user with no channels
    assert channels_list(user2["token"]) == {"channels" : []}
    
    # try to see the channels of a user that owns one public channel
    assert channels_list(user1["token"]) == { "channels" : [{
        "channel_id" : channel1["channel_id"],
        "name" : "Channel 1"
    }]}
    
    # add user2 to channel1 and check that we can list it as belonging to that
    # channel
    channel_join(user2["token"], channel1["channel_id"])
    assert channels_list(user2["token"]) == { "channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        }
    ]}
    
    # create a new channel, test that multiple channels are shown
    channel2 = channels_create(user1["token"], "Channel 2", True)
    assert channels_list(user1["token"]) == { "channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        },
    ]}
    
    # create a private channel, test that it is shown in the list
    channel3 = channels_create(user1["token"], "Channel 3", False)
    assert channels_list(user1["token"]) == { "channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        },
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        },
    ]}
    
    # test that if a channel only has one channel, and it is private, that it
    # is shown in the list
    channel_leave(user1["token"], channel1["channel_id"])
    channel_leave(user1["token"], channel2["channel_id"])
    assert channels_list(user1["token"]) == { "channels" : [
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        }
    ]}


#######################################################################
###  CHANNEL_LISTALL TESTS HERE #######################################
#######################################################################

def test_channels_listall():
    clear_data()
    
    # create some users and channels for testing, commented for now
    # until auth_register works
    user1 = auth_register("valid@email.com", "0123456789", "Bob", "Jones")
    user2 = auth_register("good@email.com", "9876543210", "Jone", "Bobs")
    
    # ensure that if there are no channels that none are shown
    assert channels_listall(user1["token"]) == {"channels" : []}
    
    channel1 = channels_create(user1["token"], "Channel 1", True)
    
    # ensure that channels_listall shows channels you belong to
    assert channels_listall(user1["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        }
    ]}
    
    # ensure that channels_listall shows channels you do not belong to
    assert channels_listall(user2["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        }
    ]}
    
    # create a new channel and repeat the above tests to make sure that multiple
    # channels are listed
    channel2 = channels_create(user1["token"], "Channel 2", True)
    
    assert channels_listall(user1["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        }
    ]}
    
    assert channels_listall(user2["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        }
    ]}
    
    
    # ensure that channels_listall shows private channels you belong to
    channel3 = channels_create(user1["token"], "Channel 3", False)
    
    assert channels_listall(user1["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        },
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        }
    ]}
    
    # ensure that channels_listall shows private channels that you do not belong
    # to
    
    assert channels_listall(user2["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        },
        {
            "channel_id" : channel2["channel_id"],
            "name" : "Channel 2"
        },
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        }
    ]}
    
    # seems to be all the testing I can think of right now, might return to this
    # if I can think of more tests