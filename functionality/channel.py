"""
Functions that relate to the creation, modification and deletion of channels.
"""
from .database import (get_data, check_valid_token, get_channel, get_user,
                       is_user_member, is_user_owner, get_message_list,
                       is_valid_u_id, message_count, Channel)
from .access_error import *


def channel_addowner(token, channel_id, u_id):
    """
    Select a user by u_id and add them to the channel owners of this channel
    """

    if not is_user_member(u_id, channel_id):
        raise AccessError(description='You do not have permission to do this')

    channel = get_channel(channel_id)
    channel_members = channel.get_members()

    # convert the channel_members list to a form the frontend can read
    users = get_data()["users"]
    
    channel_members = [{
        "u_id" : users[u_id].get_u_id(),
        "name_first" : users[u_id].get_first_name(),
        "name_last" : users[u_id].get_last_name()
    } for u_id in channel_members]

    # do the same thing with the channel owners
    channel_owners = channel.get_owners()
    channel_owners = [{
        "u_id" : users[u_id].get_u_id(),
        "name_first" : users[u_id].get_first_name(),
        "name_last" : users[u_id].get_last_name()
    } for u_id in channel_owners]

    return {"name" : channel.get_name(),
            "owner_members" : channel_owners,
            "all_members" : channel_members}


def channel_details(token, channel_id):
    """
    Select a channel by id and return its details.
    """
    u_id = check_valid_token(token)

    if not is_user_member(u_id, channel_id):
        raise AccessError(description='You do not have permission to do this')

    channel = get_channel(channel_id)
    channel_members = channel.get_members()

    # convert the channel_members list to a form the frontend can read
    users = get_data()["users"]
    
    channel_members = [{
        "u_id" : users[u_id].get_u_id(),
        "name_first" : users[u_id].get_first_name(),
        "name_last" : users[u_id].get_last_name()
    } for u_id in channel_members]

    # do the same thing with the channel owners
    channel_owners = channel.get_owners()
    channel_owners = [{
        "u_id" : users[u_id].get_u_id(),
        "name_first" : users[u_id].get_first_name(),
        "name_last" : users[u_id].get_last_name()
    } for u_id in channel_owners]

    return {"name" : channel.get_name(),
            "owner_members" : channel_owners,
            "all_members" : channel_members}



def channel_invite(token, channel_id, u_id):
    """
    Select a channel by id and user by u_id, check whether or not we
    have permission to add a new user to a channel and, if we do, add
    the new user to the list of channel members.
    """
    inviter_id = check_valid_token(token)
    channel = get_channel(channel_id)

    if not is_valid_u_id(u_id):
        raise Value_Error(description="u_id is not a real user")

    if is_user_member(u_id, channel_id):
        raise ValueError(description="User is already a member of this channel")

    if not is_user_owner(inviter_id, channel_id):
        raise AccessError(description="You do not have permission to do this")

    channel.add_member(u_id)

    return {}


def channel_join(token, channel_id):
    """
    Select a channel by id and, if it is public or we have special
    permissions, join it as a member.
    """
    u_id = check_valid_token(token)
    user = get_user(u_id)

    channel = get_channel(channel_id)

    if not channel.is_public() and not (user.is_global_admin() or
                                        user.is_slackr_owner()):
        raise AccessError("Cannot join private channel as regular\
                                   user")

    channel.add_member(u_id)

    return {}


def channel_leave(token, channel_id):
    """
    Take a channel by id and, if we are a member, leave the channe.
    Ensure that member's also lose their owner status, if the user is
    not a member fail silently.
    """
    u_id = check_valid_token(token)
    channel = get_channel(channel_id)

    # get the channel itself
    channel = get_channel(channel_id)

    # attempt to remove the user from the channel, if they are also an
    # owner of the channel remove them from tha list as well
    if is_user_member(u_id, channel_id):
        channel.get_members().remove(u_id)
    
    if is_user_owner(u_id, channel_id):
        channel.get_owners().remove(u_id)
    
    # always return an empty dictionary
    return {}


def channel_messages(token, channel_id, start):
    """
    Retrieve 50 messages from the channel referred to by channel_id
    beginning from start. Make sure messages are listed in
    chronological order and if there are no messages left set end to -1
    on the return.
    """

    channel = get_channel(channel_id)
    u_id = check_valid_token(token)

    # this will check if the user is a member of the channel.
    if not is_user_member(u_id, channel_id):
        raise AccessError("You do not have permission to do this")

    # get the amount of messages in the channel
    message_num = message_count(channel)

    if start > message_num:
        raise Value_Error(description="Start greater than the count of messages")

    # set end to start + 50 if this is less than the amount of messages
    # in the channel otherwise set it to the amount of messages left
    end = start + 50 if start + 50 < message_num else message_num

    # this function retrives a message list.
    messages = get_message_list(channel, start, end)

    return {'messages' : messages,
            'start' : start,
            'end' : end if end < message_num else -1}


def channel_removeowner(token, channel_id, u_id):
    """
    Select a channel by id and a user by id then, if we have the perms,
    remove that user from the list of channel owners. If the user is
    not an owner raise a ValueError and if we do not have permissions
    to do this raise an AccessError.
    """

    # get the data about the requesting user
    owner_uid = check_valid_token(token)
    owner = get_user(owner_uid)

    # get the channel
    to_remove = get_channel(channel_id)

    if u_id not in to_remove.get_owners():
        raise Value_Error(description="The user is not an owner of this channel")

    if owner_uid not in to_remove.get_owners() and not owner.is_global_admin():
        raise AccessError(description="You do not have permissions to do this")


    # finally remove the u_id as an owner of the channel requested, we
    # will need to interact with a database to handle this
    to_remove.get_owners().remove(u_id)

    return {}


def channels_create(token, name, is_public):
    """
    Create a new channel with the given name, if is_public is true make
    the channel public otherwise make it private. Return the id of the
    newly created channel.
    """

    # first check for a valid name
    if len(name) > 20:
        raise Value_Error(description="Channel name is too short")

    # get the u_id of this user
    u_id = check_valid_token(token)

    server_data = get_data()

    # make our channel id just be the count of channels we already have
    # incremented by 1, this way the channel_ids will increase
    # sequentially
    channel_id = len(server_data["channels"]) + 1

    # at the start there will be no messages and the only member will
    # be the creator of the channel
    new_channel = Channel(channel_id, name, [], [u_id], is_public)

    # add the channel to the server database
    server_data["channels"][channel_id] = new_channel

    # return the new channel's id
    return {"channel_id" : channel_id}


def channels_list(token):
    """
    Return a list of all the channels that the user making this request
    belongs to.
    """

    # this is pretty simple, just grab the "database"
    channels_raw = get_data()["channels"]

    u_id = check_valid_token(token)

    # use a quick list comprehension to get the channels that this u_id
    # is listed as a member of
    channels = [
        channels_raw[c_id].frontend_format() for c_id in channels_raw if u_id
        in channels_raw[c_id].get_members()
    ]

    # quick little list comprehension to return the channels in the
    # format we need
    return {"channels" : channels}


def channels_listall(token):
    """
    Return a list of all channels in the slackr.
    """

    # this is pretty simple, just grab the "database"
    channels_raw = get_data()["channels"]

    # make sure the token is valid
    check_valid_token(token)

    channels = [
        channels_raw[c_id].frontend_format() for c_id in channels_raw
    ]

    # quick little list comprehension to return the channels in the
    # format we need
    return {"channels" : channels}
