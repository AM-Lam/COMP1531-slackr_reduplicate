import pytest
from .access_error import *
from .channel_details import channel_details, verify_user_status, check_channel_existence
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .database import clear_data


def test_run_all():
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
    with pytest.raises(ValueError , match=r"*"):
        check_channel_existence(invalid_channel)

    # user2 is not a part of the channel
    with pytest.raises(AccessError , match=r"*"):
        verify_user_status(token2 ,unswchannelid)


    # adding user 2 to the channel
    channel_join(user2["token"], unswchannelid)
    
    # search details
    detaildict = channel_details(token2, unswchannelid)
    assert detaildict['name'] == "unswchannel"
    assert detaildict['owner_members'] == [1]
    assert detaildict['all_members'] == [1 , 2]
    
    # add user 3
    channel_join(user3["token"], unswchannelid)
    
    # search details
    detaildict2 = channel_details(token2, unswchannelid)
    assert detaildict2['name'] == "unswchannel"
    assert detaildict2['owner_members'] == [1]
    assert detaildict2['all_members'] == [1,2,3]
