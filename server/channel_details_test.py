import pytest
from ch_details_access_error import AccessError
import channel_details
import auth_register
import channels_create
import channel_invite



# what if the channel does not exist?
def test_channel_real():
    with pytest.raises(ValueError , match=r"*"):
        invalid_channel = 9999999999999999999999999999999999999999999999999999999999999999999
        channel_details.check_channel_existence(invalid_channel)

# user looking for details is not a member of the channel
def test_user_status():
    user1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user2 = auth_register.register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
    token1 = user1['token']
    token2 = user2['token']
    uid1 = user1['u_id']
    uid2 = user2['u_id']
    unswchannel = channels_create.channels_create(token1, unswchannel, True)
    unswchannelid = unswchannel['channel_id']
    with pytest.raises(AccessError , match=r"*"):
        channel_details.verify_user_status(token2 ,unswchannelid)   #user2 is not a part of the channel

# testing overall functionality
def test_details():
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
    unswchannel = channels_create.channels_create(token1, unswchannel, True)
    unswchannelid = unswchannel['channel_id']
    # adding user 2 to the channel
    channel_invite.channel_invite(token2, unswchannelid, uid2)
    # search details
    detaildict = channel_details.channel_details(token2, unswchannelid)
    assert(detaildict['name'] == "unswchannel")
    assert(detaildict['owner_members'] == ["user a"])
    assert(detaildict['all_members'] == ["user a" , "ussr b"])
    # add user 3
    channel_invite.channel_invite(token3, unswchannelid, uid3)
    # search details
    detaildict2 = channel_details.channel_details(token2, unswchannelid)
    assert(detaildict2['name'] == "unswchannel")
    assert(detaildict2['owner_members'] == ["user a"])
    assert(detaildict2['all_members'] == ["user a" , "ussr b" , "tha rabbit"])
