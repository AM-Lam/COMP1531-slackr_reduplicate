# pylint: disable=C0114
# pylint: disable=C0116

import pytest
from .auth import auth_register
from .message import message_send
from .channel import (channels_create, channel_addowner, channel_join,
                      channel_details, channel_invite, channel_leave,
                      channel_messages, channel_removeowner, channels_list,
                      channels_listall)
from .database import clear_data, get_channel, is_user_member, get_user
from .access_error import AccessError, Value_Error


###############################################################################
###  BOILER PLATE SETUP #######################################################
###############################################################################

def boiler_setup(function):
    clear_data()
    server_data = get_data()
    user_1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user_2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
    user_3 = auth_register('user3@domain.com.au' , 'vsdco23111' , 'person' , 'c')
    assert user_1 is not None
    assert user_2 is not None
    assert user_3 is not None

    token_1 = user_1['token']
    token_2 = user_2['token']
    token_3 = user_3['token']

    uid_1 = user_1['u_id']
    uid_2 = user_2['u_id']
    uid_3 = user_3['u_id']


    channel_1 = channels_create(user_1["token"], "Channel 1", True)
    channel_2 = channels_create(user_1["token"], "Channel 2", True)
    channel_2a = channels_create(user_1["token"], "Channel 2a", False)
    channel_3 = channels_create(user_1["token"], "Good 'Ol Channel", True)
    unswchannel = channels_create(token_1, 'unswchannel', True)
    usydchannel = channels_create(token_1, 'usydchannel', True)
    yeetchannel = channels_create(token_1, 'yeetchannel', True)
    unichannel = channels_create(token_1, 'unichannel', True)
   
    unichannelid = unichannel['channel_id']
    yeetchannelid = yeetchannel['channel_id']
    usydchannelid = usydchannel['channel_id']
    unswchannelid = unswchannel['channel_id']
    def wrapper():
        return function
    return wrapper


###############################################################################
###  CHANNEL_ADDOWNER TESTS HERE ##############################################
###############################################################################

@boiler_setup
def test_channel_addowner():
    # first add a user as an owner to a channel we own
    assert channel_addowner(user_1["token"], channel_1["channel_id"], user_2["u_id"]) == {}
    
    # now ensure that we can add a user to a channel as an owner after we have
    # been added to it as an owner ourselves (ensure the adding is actually
    # working properly)
    assert channel_addowner(user_2["token"], channel_1["channel_id"], user_3["u_id"]) == {}
    
    # try to add a user as an owner to a channel they are already an owner
    # on
    pytest.raises(Value_Error, channel_addowner, user_1["token"], channel_1["channel_id"], user_2["u_id"])
    
    # try to add a user as an owner to a channel we do not own
    pytest.raises(AccessError, channel_addowner, user_2["token"], channel_2["channel_id"], user_3["u_id"])
    
    
    # try to add a user as an owner to a channel we do not own, as a slackr 
    # owner

    # somehow make user2 an owner of the slackr, commented until we add global
    # admins
    # assert channel_addowner(user2["token"], channel2["channel_id"],
    #                         user3["u_id"]) == {}


###############################################################################
###  CHANNEL_DETAILS TESTS HERE ###############################################
###############################################################################

@boiler_setup
def test_channel_details():
    # what if the channel does not exist?
    invalid_channel = 999
    with pytest.raises(Value_Error, match=r"*"):
        get_channel(invalid_channel)

    # user2 is not a part of the channel
    assert is_user_member(user_2["u_id"], unswchannel["channel_id"]) == False

    # adding user 2 to the channel
    channel_join(user_2["token"], unswchannelid)
    
    # search details
    detaildict = channel_details(token_2, unswchannelid)
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
        {'u_id': 3, 'name_first': 'person', 'name_last': 'c'}]


###############################################################################
###  CHANNEL_INVITE TESTS HERE ################################################
###############################################################################

@boiler_setup
def test_channel_invite():
    # lets create an invalid non existant user id
    uidfaux = 999999999999999999999999999999999999999999999999999999999999999999

    # test if the user is valid.
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite('3131313133', unswchannelid, uid_2)

    # test if user does not exist on application database
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token_1, unswchannelid, 'jl mackie')

    # user exists but is already a part of that channel then invite should raise Value_Error
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token_1, unswchannelid, uid_1)

    # what if the channel does not exist?
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token_1, "this channel does not exist", uid_2)

    # add user 2 to the channel (invitee -> user 1)
    channel_invite(token_1, unswchannelid, uid_2)
    # user 2 is already a part of that channel the invite should raise Value_Error
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(token_1, unswchannelid, uid_2)


###############################################################################
###  CHANNEL_JOIN TESTS HERE ##################################################
###############################################################################

@boiler_setup
def test_channel_join():

    # first try to join a public server that exists
    assert channel_join(user_2['token'], channel_1['channel_id']) == {}
    
    # now try to join a server that does not exist, this should fail with an
    # access error
    pytest.raises(Value_Error, channel_join, user_2['token'], 404)
    
    # try to join a server that exists, but is private as a regular user
    pytest.raises(AccessError, channel_join, user_2['token'], 
                  channel_2a['channel_id'])
    
    # try to join a server that exists, but is private as an admin
    # first we'll have to make the second user an admin, not sure how this will
    # work yet
    pytest.raises(AccessError, channel_join, user_2['token'], 
                  channel_2a['channel_id'])


###############################################################################
###  CHANNEL_LEAVE TESTS HERE #################################################
###############################################################################

@boiler_setup
def test_channel_leave():
    # first check the simplest case, if the user can leave a channel they are in
    assert channel_leave(user_1["token"], channel_1["channel_id"]) == {}

    # now try to leave a private channel
    assert channel_leave(user_1["token"], channel_2a["channel_id"]) == {}

    # now check that attempting to leave a non-existent channel raises an
    # exception
    pytest.raises(Value_Error, channel_leave, user_1["token"], 404)

    # try to leave a channel the user is not a part of - this should fail
    # quietely (see assumptions.md)
    assert channel_leave(user_1["token"], channel_3["channel_id"]) == {}


###############################################################################
###  CHANNEL_MESSAGES TESTS HERE ##############################################
###############################################################################

@boiler_setup
def test_channel_messages():
    # start greater than the total number of messages#########
    # adding user 2 and 3 to the unsw channel
    channel_invite(token_1, unswchannelid, uid_2)
    channel_invite(token_1, unswchannelid, uid_3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token_1, unswchannelid, messageloop)
    # now lets call channel messages...
    with pytest.raises(Value_Error, match=r"*"):
        channel_messages(token_1, unswchannelid, 93)

    # INVALID USER TEST###################
    # adding  ONLY user 2 to the channel
    channel_invite(token_1, usydchannelid, uid_2)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token_1, usydchannelid, messageloop)
    # now lets call channel messages...
    with pytest.raises(AccessError, match=r"*"):
        channel_messages(token_3, usydchannelid, 2)

    # END SHOULD BE -1 AS THE LEAST RECENT MESSAGE WAS SENT OUT######
    # adding user 2 and 3 to the channel
    channel_invite(token_1, yeetchannelid, uid_2)
    channel_invite(token_1, yeetchannelid, uid_3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token_1, yeetchannelid, messageloop)
    # now lets call channel messages...
    mesdict = channel_messages(token_1, yeetchannelid, 40)
    assert mesdict['start'] == 40
    assert mesdict['end'] == -1

    # SOME IN BETWEEN INTERVAL TESTING
    # adding user 2 and 3 to the channel
    channel_invite(token_1, unichannelid, uid_2)
    channel_invite(token_1, unichannelid, uid_3)
    # lets send 70 messages.......
    initmessage = 'lots of'
    for i in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(token_1, unichannelid, messageloop)
    # now lets call channel messages...
    mesdict1 = channel_messages(token_1, unichannelid, 10)
    assert mesdict1['start'] == 10
    assert mesdict1['end'] == 60


###############################################################################
###  CHANNEL_REMOVEOWNER TESTS HERE ###########################################
###############################################################################

@boiler_setup
def test_channel_removeowner():
    user3_obj = get_user(user_3["u_id"])

    # now add user2 as an owner to channel1
    channel_addowner(user_1["token"], channel_1["channel_id"], user_2["u_id"])
    
    # test removing user2 as an owner
    assert channel_removeowner(user_1["token"], channel_1["channel_id"],
                               user_2["u_id"]) == {}
    
    # test removing user2 when they are not an owner
    pytest.raises(Value_Error, channel_removeowner, user_1["token"],
                  channel_1["channel_id"], user_2["u_id"])
    
    # add user2 as an owner to channel1 again
    channel_addowner(user_1["token"], channel_1["channel_id"], user_2["u_id"])
    
    # attempt to remove user2 from channel1 as a user that does not have permis
    # -sions to do so
    pytest.raises(AccessError, channel_removeowner, user_3["token"], 
                  channel_1["channel_id"], user_2["u_id"])
    
    # test removing user2 from channel1 as a slackr owner
    user3_obj.set_global_admin(True)
    assert channel_removeowner(user_3["token"], channel_1["channel_id"],
                               user_2["u_id"]) == {}
    
    # try to remove an owner from a channel that does not exist
    pytest.raises(Value_Error, channel_removeowner, user_1["token"], 128,
                  user_2["u_id"])


###############################################################################
###  CHANNEL_CREATE TESTS HERE ################################################
###############################################################################

@boiler_setup
def test_channels_create():

    # try to create a valid, public channel
    assert channels_create(user_1["token"], "Channel 1", True) == {"channel_id" : 1}

    # try to create a valid, private channel
    assert channels_create(user_1["token"], "Channel 1", True) == {"channel_id" : 2}
    
    # try to create a channel with an invalid name
    pytest.raises(Value_Error, channels_create, user_1["token"], 
                  "123456789012345678901", False)


###############################################################################
###  CHANNEL_LIST TESTS HERE ##################################################
###############################################################################

# did not use the decorator here because the tests progress as the database builds up!
def test_channels_list():
    clear_data()

    # boilerplate user/channel creation code
    user1 = auth_register("valid@email.com", "123456789", "Bob", "Jones")
    user2 = auth_register("new@email.com", "987654321", "Doug", "Jones")

    channel1 = channels_create(user1["token"], "Channel 1", True)

    # try to see the channels of a user with no channels
    assert channels_list(user2["token"]) == {"channels" : []}

    # try to see the channels of a user that owns one public channel
    assert channels_list(user1["token"]) == {"channels" : [{
        "channel_id" : channel1["channel_id"],
        "name" : "Channel 1"
    }]}

    # add user2 to channel1 and check that we can list it as belonging to that
    # channel
    channel_join(user2["token"], channel1["channel_id"])
    assert channels_list(user2["token"]) == {"channels" : [
        {
            "channel_id" : channel1["channel_id"],
            "name" : "Channel 1"
        }
    ]}

    # create a new channel, test that multiple channels are shown
    channel2 = channels_create(user1["token"], "Channel 2", True)
    assert channels_list(user1["token"]) == {"channels" : [
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
    assert channels_list(user1["token"]) == {"channels" : [
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
    assert channels_list(user1["token"]) == {"channels" : [
        {
            "channel_id" : channel3["channel_id"],
            "name" : "Channel 3"
        }
    ]}


###############################################################################
###  CHANNEL_LISTALL TESTS HERE ###############################################
###############################################################################

# did not use the decorator here because the tests progress as the database builds up!
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