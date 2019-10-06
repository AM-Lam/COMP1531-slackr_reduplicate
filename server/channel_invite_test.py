import auth_register
import auth_login
import channels_create
import channel_join
import channel_invite


# first we create two users:
user1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
user2 = auth_register.auth_register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
token1 = user1['token']
token2 = user2['token']
uid1 = user1['u_id']
uid2 = user2['u_id']

# lets create an invalid non existant user id
uidfaux = 999999999999999999999999999999999999999999999999999999999999999999

# now we create a channel
unswchannel = channel_create.channels_create(token1, unswchannel, True)
unswchannelid = unswchannel['channel_id']
# user1 is now a part of unswchannel

# test if user does not exist on application database
def test_verify_user_validity():
     with pytest.raises(ValueError , match=r"*"):
        channel_invite.verify_user_validity(uidfaux)

# user exists but is already a part of that channel then invite should raise valueError
def test_verify_token_not_member():
    with pytest.raises(ValueError , match=r"*"):
        channel_invite.verify_token_not_member(token1, unswchannelid, uid1)



