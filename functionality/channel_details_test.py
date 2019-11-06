import pytest
from .auth import auth_register
from .channel import channel_join, channels_create, channel_details
from .database import clear_data, get_channel, is_user_member
from .access_error import AccessError, Value_Error


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
