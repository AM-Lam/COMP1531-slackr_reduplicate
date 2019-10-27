import pytest
from .access_error import AccessError
from .channel_details import *
from .auth_register import *
from .channels_create import *
from .channel_invite import *

############################################################################################################################################################

#initialisation
user1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
user2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
user3 = auth_register('user3@domain.com' , 'lollollmao' , 'the' , 'rabbit')
token1 = user1['token']
token2 = user2['token']
token3 = user3['token']
uid1 = user1['u_id']
uid2 = user2['u_id']
uid3 = user3['u_id']
# user1 will be the channel owner
unswchannel = channels_create(token1, 'unswchannel', True)
unswchannelid = unswchannel['channel_id']

###########################################################################################################################################################

# what if the channel does not exist?
def test_channel_real():
    with pytest.raises(ValueError , match=r"*"):
        invalid_channel = 9999999999999999999999999999999999999999999999999999999999999999999
        check_channel_existence(invalid_channel)

# user looking for details is not a member of the channel
def test_user_status():
    with pytest.raises(AccessError , match=r"*"):
        verify_user_status(token2 ,unswchannelid)   #user2 is not a part of the channel

###########################################################################################################################################################

# testing overall functionality
def test_details():
    # adding user 2 to the channel
    channel_invite(token1, unswchannelid, uid2)
    # search details
    detaildict = channel_details(token2, unswchannelid)
    assert(detaildict['name'] == "unswchannel")
    assert(detaildict['owner_members'] == [1])
    assert(detaildict['all_members'] == [1 , 2])
    # add user 3
    channel_invite(token2, unswchannelid, uid3)
    # search details
    detaildict2 = channel_details(token2, unswchannelid)
    assert(detaildict2['name'] == "unswchannel")
    assert(detaildict2['owner_members'] == [1])
    assert(detaildict2['all_members'] == [1,2,3])
