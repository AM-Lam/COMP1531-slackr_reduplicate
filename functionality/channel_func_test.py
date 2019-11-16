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
from .decorators import setup_data
from .access_error import AccessError, Value_Error


###############################################################################
###  CHANNEL_ADDOWNER TESTS HERE ##############################################
###############################################################################


@setup_data(user_num=3, channel_num=2)
def test_channel_addowner(users, channels):
    # first add a user as an owner to a channel we own
    assert channel_addowner(users[0]["token"], channels[0]["channel_id"],
                            users[1]["u_id"]) == {}
    
    # now ensure that we can add a user to a channel as an owner after we have
    # been added to it as an owner ourselves (ensure the adding is actually
    # working properly)
    assert channel_addowner(users[1]["token"], channels[0]["channel_id"],
                            users[2]["u_id"]) == {}
    
    # try to add a user as an owner to a channel they are already an owner
    # on
    pytest.raises(Value_Error, channel_addowner, users[0]["token"],
                  channels[0]["channel_id"], users[1]["u_id"])
    
    # try to add a user as an owner to a channel we do not own
    pytest.raises(AccessError, channel_addowner, users[1]["token"],
                  channels[1]["channel_id"], users[2]["u_id"])
    
    
    # try to add a user as an owner to a channel we do not own, as a slackr 
    # owner

    # somehow make user2 an owner of the slackr, commented until we add global
    # admins
    # assert channel_addowner(user2["token"], channel2["channel_id"],
    #                         user3["u_id"]) == {}


###############################################################################
###  CHANNEL_DETAILS TESTS HERE ###############################################
###############################################################################

@setup_data(user_num=4, channel_num=1)
def test_channel_details(users, channels):
    # what if the channel does not exist?
    invalid_channel = 999
    with pytest.raises(Value_Error, match=r"*"):
        get_channel(invalid_channel)

    # user2 is not a part of the channel
    assert is_user_member(users[1]["u_id"], channels[0]["channel_id"]) == False

    # adding user 2 to the channel
    channel_join(users[1]["token"], channels[0]["channel_id"])
    
    # search details
    detaildict = channel_details(users[1]["token"], channels[0]["channel_id"])
    assert detaildict['name'] == "Channel 1"
    assert detaildict['owner_members'] == [
        {'u_id': 1, 'name_first': 'user1', 'name_last': 'last1'}]

    assert detaildict['all_members'] == [
        {'u_id': 1, 'name_first': 'user1', 'name_last': 'last1'},
        {'u_id': 2, 'name_first': 'user2', 'name_last': 'last2'}]

    # add user 3
    channel_join(users[2]["token"], channels[0]["channel_id"])

    # search details
    detaildict2 = channel_details(users[1]["token"], channels[0]["channel_id"])
    assert detaildict2['name'] == "Channel 1"

    assert detaildict2['owner_members'] == [
        {'u_id': 1, 'name_first': 'user1', 'name_last': 'last1'}]

    assert detaildict2['all_members'] == [
        {'u_id': 1, 'name_first': 'user1', 'name_last': 'last1'},
        {'u_id': 2, 'name_first': 'user2', 'name_last': 'last2'},
        {'u_id': 3, 'name_first': 'user3', 'name_last': 'last3'}]
    
    # try to get the details of a channel we do not have access to
    pytest.raises(AccessError, channel_details, users[3]["token"],
                  channels[0]["channel_id"])


###############################################################################
###  CHANNEL_INVITE TESTS HERE ################################################
###############################################################################

@setup_data(user_num=3, channel_num=1)
def test_channel_invite(users, channels):
    # test if the user is invalid.
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite('3131313133', channels[0]["channel_id"],
                       users[0]["u_id"])

    # test if user does not exist on application database
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(users[0]["token"], channels[0]["channel_id"],
                       'jl mackie')

    # user exists but is already a part of that channel then invite
    # should raise Value_Error
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(users[0]["token"], channels[0]["channel_id"],
                       users[0]["u_id"])

    # what if the channel does not exist?
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(users[0]["token"], "does not exist",
                       users[0]["u_id"])

    # add user 2 to the channel (invitee -> user 1)
    channel_invite(users[0]["token"], channels[0]["channel_id"], users[1]["u_id"])

    # user 2 is already a part of that channel the invite should raise
    # Value_Error
    with pytest.raises(Value_Error , match=r"*"):
        channel_invite(users[0]["token"], "does not exist", users[1]["u_id"])
    
    # try to invite a user to a channel that we are not an owner of
    pytest.raises(AccessError, channel_invite, users[1]["token"],
                  channels[0]["channel_id"], users[2]["u_id"])


###############################################################################
###  CHANNEL_JOIN TESTS HERE ##################################################
###############################################################################

@setup_data(user_num=2, channel_num=2, public=[True, False])
def test_channel_join(users, channels):

    # first try to join a public server that exists
    assert channel_join(users[1]['token'], channels[0]['channel_id']) == {}
    
    # now try to join a server that does not exist, this should fail with an
    # access error
    pytest.raises(Value_Error, channel_join, users[1]['token'], 404)
    
    # try to join a server that exists, but is private as a regular user
    pytest.raises(AccessError, channel_join, users[1]['token'], 
                  channels[1]['channel_id'])
    
    # try to join a server that exists, but is private as an admin
    # first we'll have to make the second user an admin, not sure how this will
    # work yet
    user2 = get_user(users[1]["u_id"])
    user2.set_global_admin(True)

    assert channel_join(users[1]['token'], channels[1]['channel_id']) == {}


###############################################################################
###  CHANNEL_LEAVE TESTS HERE #################################################
###############################################################################

@setup_data(user_num=2, channel_num=3, public=[True, False, True], creators=[0, 0, 1])
def test_channel_leave(users, channels):
    # first check the simplest case, if the user can leave a channel they are in
    assert channel_leave(users[0]["token"], channels[0]["channel_id"]) == {}

    # now try to leave a private channel
    assert channel_leave(users[0]["token"], channels[1]["channel_id"]) == {}

    # now check that attempting to leave a non-existent channel raises an
    # exception
    pytest.raises(Value_Error, channel_leave, users[0]["token"], 404)

    # try to leave a channel the user is not a part of - this should fail
    # quietely (see assumptions.md)
    assert channel_leave(users[0]["token"], channels[2]["channel_id"]) == {}


###############################################################################
###  CHANNEL_MESSAGES TESTS HERE ##############################################
###############################################################################

@setup_data(user_num=3, channel_num=4)
def test_channel_messages(users, channels):
    # start greater than the total number of messages
    # adding user 2 and 3 to the unsw channel
    channel_invite(users[0]["token"], channels[0]["channel_id"], users[1]["u_id"])
    channel_invite(users[0]["token"], channels[0]["channel_id"], users[2]["u_id"])

    # lets send 70 messages.......
    initmessage = 'lots of'
    for _ in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(users[0]["token"], channels[0]["channel_id"], messageloop)

    # now lets call channel messages...
    with pytest.raises(Value_Error, match=r"*"):
        channel_messages(users[0]["token"], channels[0]["channel_id"], 93)

    # INVALID USER TEST
    # adding  ONLY user 2 to the channel
    channel_invite(users[0]["token"], channels[1]["channel_id"], users[1]["u_id"])

    # lets send 70 messages...
    initmessage = 'lots of'
    for _ in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(users[0]["token"], channels[1]["channel_id"], messageloop)

    # now lets call channel messages...
    with pytest.raises(AccessError, match=r"*"):
        channel_messages(users[2]["token"], channels[1]["channel_id"], 2)

    # END SHOULD BE -1 AS THE LEAST RECENT MESSAGE WAS SENT OUT
    # adding user 2 and 3 to the channel
    channel_invite(users[0]["token"], channels[2]["channel_id"], users[1]["u_id"])
    channel_invite(users[0]["token"], channels[2]["channel_id"], users[2]["u_id"])

    # lets send 70 messages...
    initmessage = 'lots of'
    for _ in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(users[0]["token"], channels[2]["channel_id"], messageloop)

    # now lets call channel messages...
    mesdict = channel_messages(users[0]["token"], channels[2]["channel_id"], 40)
    assert mesdict['start'] == 40
    assert mesdict['end'] == -1

    # SOME IN BETWEEN INTERVAL TESTING
    # adding user 2 and 3 to the channel
    channel_invite(users[0]["token"], channels[3]["channel_id"], users[1]["u_id"])
    channel_invite(users[0]["token"], channels[3]["channel_id"], users[2]["u_id"])

    # lets send 70 messages...
    initmessage = 'lots of'
    for _ in range(0, 70):
        messageloop = initmessage + ' aa'
        message_send(users[0]["token"], channels[3]["channel_id"], messageloop)

    # now lets call channel messages...
    mesdict1 = channel_messages(users[0]["token"], channels[3]["channel_id"], 10)
    assert mesdict1['start'] == 10
    assert mesdict1['end'] == 60


###############################################################################
###  CHANNEL_REMOVEOWNER TESTS HERE ###########################################
###############################################################################

@setup_data(user_num=3, channel_num=1)
def test_channel_removeowner(users, channels):
    user3_obj = get_user(users[2]["u_id"])

    # now add user2 as an owner to channel1
    channel_addowner(users[0]["token"], channels[0]["channel_id"], users[1]["u_id"])
    
    # test removing user2 as an owner
    assert channel_removeowner(users[0]["token"], channels[0]["channel_id"],
                               users[1]["u_id"]) == {}
    
    # test removing user2 when they are not an owner
    pytest.raises(Value_Error, channel_removeowner, users[0]["token"],
                  channels[0]["channel_id"], users[1]["u_id"])
    
    # add user2 as an owner to channel1 again
    channel_addowner(users[0]["token"], channels[0]["channel_id"], users[1]["u_id"])
    
    # attempt to remove user2 from channel1 as a user that does not have permis
    # -sions to do so
    pytest.raises(AccessError, channel_removeowner, users[2]["token"], 
                  channels[0]["channel_id"], users[1]["u_id"])
    
    # test removing user2 from channel1 as a slackr owner
    user3_obj.set_global_admin(True)
    assert channel_removeowner(users[2]["token"], channels[0]["channel_id"],
                               users[1]["u_id"]) == {}
    
    # try to remove an owner from a channel that does not exist
    pytest.raises(Value_Error, channel_removeowner, users[0]["token"], 128,
                  users[1]["u_id"])


###############################################################################
###  CHANNEL_CREATE TESTS HERE ################################################
###############################################################################

@setup_data(user_num=1)
def test_channels_create(users, channels):
    # try to create a valid, public channel
    assert channels_create(users[0]["token"], "Channel 1", True) == {"channel_id" : 1}

    # try to create a valid, private channel
    assert channels_create(users[0]["token"], "Channel 1", True) == {"channel_id" : 2}
    
    # try to create a channel with an invalid name
    pytest.raises(Value_Error, channels_create, users[0]["token"], 
                  "123456789012345678901", False)


###############################################################################
###  CHANNEL_LIST TESTS HERE ##################################################
###############################################################################

# did not use the decorator here because the tests progress as the
# database builds up!
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

# did not use the decorator here because the tests progress as the
# database builds up!
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
