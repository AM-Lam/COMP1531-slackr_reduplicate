"""
Functions that relate to the creation, modification and deletion of channels.
"""
import jwt
from .database import get_data, get_secret, Channel, check_valid_token, get_channel, is_valid_u_id, is_user_member, is_user_owner, message_count, get_message_list
from .access_error import AccessError, ValueError


def channel_addowner(token, channel_id, u_id):
    """
    Select a user by u_id and add them to the channel owners of this channel
    """
    server_data = get_data()

    # first check whether or not the token is valid, since
    # auth_register is not yet complete just always pass this test
    if not server_data["tokens"].get(token, False):
        raise AccessError("Token not valid")

    # first get the u_id from the user token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    owner_u_id = token_payload["u_id"]

    to_add = None
    # now check whether or not the channel actually exists, if it does
    # exist set it to a value and break out of the loop earlier
    for channel in server_data["channels"]:
        if channel.get_id() == channel_id:
            to_add = channel
            break

    # if the channel requested does not exist or the u_id is already an
    # owner of it raise an error, this will probably need to interact
    # with a database
    if to_add is None:
        raise ValueError(description="The channel requested does not exist")

    if u_id in to_add.get_owners():
        raise ValueError(description="The user is already an owner in this channel")

    # now make sure the calling user has the permissions to make this
    # change, we will need a few functions to be written that access a
    # database for this to work
    if owner_u_id not in to_add.get_owners():
        raise AccessError(description="Lack permissions to add owner to this channel")

    # finally set the u_id to be an owner of the channel requested
    to_add.get_owners().append(u_id)
    if u_id not in to_add.get_members():
        to_add.get_members().append(u_id)

    return {}


def channel_details(token, channel_id):
    u_id = check_valid_token(token)
    channel = get_channel(channel_id)
    
    channel_members = channel.get_members()

    if u_id not in channel_members:
        raise AccessError(description='You do not have permission to do this')
    
    # TODO: Rewrite this to not be awful, will likely require
    # rethinking our data structures
    
    # convert the channel_members list to a form the frontend can read
    channel_members = [{
        "u_id" : user.get_u_id(),
        "name_first" : user.get_first_name(),
        "name_last" : user.get_last_name()
    } for user in get_data()["users"] if user.get_u_id() in channel_members]
    
    # do the same thing with the channel owners
    channel_owners = channel.get_owners()
    channel_owners = [{
        "u_id" : user.get_u_id(),
        "name_first" : user.get_first_name(),
        "name_last" : user.get_last_name()
    } for user in get_data()["users"] if user.get_u_id() in channel_owners]
    
    return {"name" : channel.get_name(), 
            "owner_members" : channel_owners,
            "all_members" : channel_members}


def channel_invite(token, channel_id, u_id):
    inviter_id = check_valid_token(token)
    channel = get_channel(channel_id)

    if not is_valid_u_id(u_id):
        raise ValueError(description="u_id is not a real user")

    if is_user_member(u_id, channel_id):
        raise ValueError(description="User is already a member of this channel")
    
    if not is_user_owner(inviter_id, channel_id):
        raise AccessError(description="You do not have permission to do this")
    
    channel.add_member(u_id)

    return {}


def channel_join(token, channel_id):
    server_data = get_data()

    # if the token is invalid throw an access error, since
    # auth_register is not complete just assume all tokens
    # are valid
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # next we have to check whether or not the given user is an admin,
    found_channel = False

    for channel in server_data["channels"]:
        # somehow check if the channel is private, another database
        # interaction it should probably look like what's below
        if channel.get_id() == channel_id:
            # we currently have no checks forglobal admins
            if not channel.is_public():
                raise AccessError("Cannot join private channel as regular\
                                   user")
            found_channel = True
            break

    if not found_channel:
        raise ValueError

    # add the user's u_id to the channel's list of members, since the
    # data we get using channels_listall appears to be read-only
    channel.get_members().append(u_id)

    return {}


def channel_leave(token, channel_id):
    # somehow get the associated uid, this will presumably need
    # to interact with a database or something similar
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    server_data = get_data()

    # try to remove the user from the channel, if they are not in the
    # channel then just return without any error
    for c in server_data["channels"]:
        if c.get_id() == channel_id:
            if u_id in c.get_members():
                c.get_members().remove(u_id)
            return {}

    # if we get here the channel does not exist and we need to raise an
    # exception
    raise ValueError


def channel_messages(token, channel_id, start):    
    channel = get_channel(channel_id)
    u_id = check_valid_token(token)

    # this will check if the user is a member of the channel.
    if not is_user_member(u_id, channel_id):
        raise AccessError("You do not have permission to do this")

    # get the amount of messages in the channel
    message_num = message_count(channel)

    if start > message_num:
        raise ValueError(description="Start greater than the count of messages")

    # set end to start + 50 if this is less than the amount of messages
    # in the channel otherwise set it to the amount of messages left
    end = start + 50 if start + 50 < message_num else message_num

    # this function retrives a message list.
    messages = get_message_list(channel, start, end)

    return {'messages' : messages,
            'start' : start,
            'end' : end if end < message_num else -1}


def channel_removeowner(token, channel_id, u_id):
    server_data = get_data()

    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # first get the u_id from the user token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    owner_uid = token_payload['u_id']

    owner = None
    for u in server_data["users"]:
        if u.get_u_id() == owner_uid:
            owner = u
            break

    to_remove = None
    # now check whether or not the channel actually exists, if it does
    # exist set it to a value and break out of the loop earlier
    for channel in server_data["channels"]:
        if channel.get_id() == channel_id:
            to_remove = channel
            break

    # if the channel requested does not exist or the u_id is not an
    # owner of it raise an error
    if to_remove is None:
        raise ValueError(description="The requested channel does not exist")

    if u_id not in to_remove.get_owners():
        raise ValueError(description="The user is not an owner of this channel")

    if owner_uid not in to_remove.get_owners() and not owner.is_global_admin():
        raise AccessError(description="You do not have permissions to do this")


    # finally remove the u_id as an owner of the channel requested, we
    # will need to interact with a database to handle this
    to_remove.get_owners().remove(u_id)

    return {}


def channels_create(token, name, is_public):
    # first check for a valid name
    if len(name) > 20:
        raise ValueError(description="Channel name is too short")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    server_data = get_data()

    # make our channel id just be the count of channels we already have
    # incremented by 1, this way the channel_ids will increase
    # sequentially
    channel_id = len(server_data["channels"])

    # at the start there will be no messages and the only member will
    # be the creator of the channel
    new_channel = Channel(channel_id, name, [], [u_id], is_public)

    # add the channel to the server database
    server_data["channels"].append(new_channel)

    # return the new channel's id
    return {"channel_id" : channel_id}


def channels_list(token):
    # this is pretty simple, just grab the "database"
    database = get_data()

    # if the token is not valid throw an AccessError
    if not database["tokens"].get(token, False):
        raise AccessError(description="invalid token")

    # get the user's u_id
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    channels = [
        c.frontend_format() for c in database["channels"] if u_id in c.get_members()
    ]

    # quick little list comprehension to return the channels in the
    # format we need
    return {"channels" : channels}


def channels_listall(token):
    # this is pretty simple, just grab the "database"
    database = get_data()

    # if the token is not valid throw an AccessError
    if not database["tokens"].get(token, False):
        raise AccessError(description="Invalid token")

    # quick little list comprehension to return the channels in the
    # format we need
    return {"channels" : [c.frontend_format() for c in database["channels"]]}
