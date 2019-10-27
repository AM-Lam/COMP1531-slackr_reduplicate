from .auth_register import *
from .channels_create import *
from .channel_join import *
from .channel_invite import *
from .database import *
import pytest




def test_run_first():
    clear_data()
    # first we create two users:
    user1 = auth_register('user1@domain.com' , 'passew@321', 'user' , 'a')
    user2 = auth_register('user2@domain.com' , 'vscod231343', 'ussr' , 'b')
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
    with pytest.raises(ValueError , match=r"*"):
        channel_invite('3131313133', unswchannelid, uid2)

    # test if user does not exist on application database
    with pytest.raises(ValueError , match=r"*"):
        verify_user_validity(uidfaux)

    # user exists but is already a part of that channel then invite should raise valueError
    with pytest.raises(ValueError , match=r"*"):
        verify_token_not_member(token1, unswchannelid, uid1)

    # what if the channel does not exist?
    with pytest.raises(ValueError , match=r"*"):
        verify_channel_exists(17171771717171717)

    # add user 2 to the channel (invitee -> user 1)
    channel_invite(token1, unswchannelid, uid2)
    # user 2 is already a part of that channel the invite should raise valueError
    with pytest.raises(ValueError , match=r"*"):
        verify_token_not_member(token1, unswchannelid, uid2)



