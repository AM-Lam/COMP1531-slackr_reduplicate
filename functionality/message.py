"""
Functions dealing with creating, deleting, modifying and sending
messages
"""

# pylint: disable=C0116

import threading
from datetime import datetime
from .database import (check_valid_token, get_data, get_channel,
                       is_user_member, is_user_owner, get_user, Messages)
from .access_error import AccessError, Value_Error


def send_message(channel, message, time_sent):
    # wait until we have passed beyond the desired time to send the message
    while datetime.utcnow() < time_sent:
        continue

    # now just append the message we created earlier to the provided channel
    channel.add_message(message)


def message_send(token, channel_id, message):
    # Message is more than 1000 characters
    if len(message) > 1000:
        raise Value_Error(description="Messages must be less than 1000 characters")

    # now grab the u_id associated with the provided token and the
    # channel object
    u_id = check_valid_token(token)
    channel = get_channel(channel_id)

    if not is_user_member(u_id, channel_id):
        raise AccessError(description="You don't have access in this channel")

    # now create the message we will be sending
    message_id = channel.get_m_id()
    to_send = Messages(message_id, u_id, message, channel_id,
                       datetime.utcnow(), [])

    # increment the channel's max message id
    channel.increment_m_id()

    send_message(channel, to_send, datetime.utcnow())

    # return the new message's id
    return {"message_id" : message_id}


def message_sendlater(token, channel_id, message, time_sent):
    # Message is more than 1000 characters
    if len(message) > 1000:
        raise Value_Error(description="Messages must be less than 1000 characters")

    # now grab the u_id associated with the provided token and the
    # channel object
    u_id = check_valid_token(token)
    channel = get_channel(channel_id)

    if not is_user_member(u_id, channel_id):
        raise AccessError(description="You don't have access in this channel")

    # if the time to send is in the past raise an error
    if time_sent < datetime.utcnow():
        raise Value_Error(description="Cannot send a message in the past")

    # now create the message we will be sending
    message_id = channel.get_m_id()
    to_send = Messages(message_id, u_id, message, channel_id,
                       datetime.utcnow(), [])

    # increment the channel's max message id
    channel.increment_m_id()

    # start a thread that will call send_message
    threading.Thread(target=send_message, args=(channel, to_send, time_sent)).start()

    return {"message_id" : message_id}


def message_edit(token, message_id, message):
    channels = get_data()["channels"]

    u_id = check_valid_token(token)
    request_user = get_user(u_id)

    message_user = None
    channel = None
    to_edit = None

    for channel_id in channels:
        potential_channel = get_channel(channel_id)

        try:
            to_edit = potential_channel.get_message(message_id)
            channel = potential_channel
            message_user = get_user(to_edit.get_u_id())
            break
        except Value_Error:
            continue

    if to_edit is None:
        raise Value_Error(description="Message does not exist")

    if channel is None:
        raise Value_Error(description="Channel does not exist")

    # if user is not the poster or admin
    if request_user != message_user and not request_user.is_global_admin():
        raise AccessError(description="You do not have permission to edit this message")

    # update the database with new message
    to_edit.edit_text(message)

    return {}


def message_remove(token, message_id):
    channels = get_data()["channels"]

    u_id = check_valid_token(token)
    request_user = get_user(u_id)

    message_user = None
    channel = None
    message = None

    for channel_id in channels:
        potential_channel = get_channel(channel_id)

        try:
            message = potential_channel.get_message(message_id)
            channel = potential_channel
            message_user = get_user(message.get_u_id())
            break
        except Value_Error:
            continue

    if message is None:
        raise Value_Error(description="Message does not exist")

    if channel is None:
        raise Value_Error(description="Channel does not exist")

    # if user is not the poster or admin
    if request_user != message_user and not request_user.is_global_admin():
        raise AccessError(description="You do not have permission to edit this message")

    # remove the message to the server database
    channel.remove_message(message)

    return {}


def message_pin(token, message_id):
    channels = get_data()["channels"]

    u_id = check_valid_token(token)

    user = get_user(u_id)

    channel = None
    message = None

    for channel_id in channels:
        potential_channel = get_channel(channel_id)

        try:
            message = potential_channel.get_message(message_id)
            channel = potential_channel
            break
        except Value_Error:
            continue

    if message is None:
        raise Value_Error(description="Message does not exist")

    if channel is None:
        raise Value_Error(description="Channel does not exist")

    if not user.is_global_admin() and not is_user_owner(u_id, channel.get_id()):
        raise Value_Error(description="Only admins and owners can pin messages!")

    # Message with ID message_id is already pinned raises an error
    if message.is_pinned():
        raise Value_Error(description="The message is already pinned")

    # otherwise pin the message and add it to the channels list of
    # pins
    message.set_pinned(True)
    channel.add_pin(message_id)

    return {}


def message_unpin(token, message_id):
    channels = get_data()["channels"]

    u_id = check_valid_token(token)
    user = get_user(u_id)

    channel = None
    message = None

    for channel_id in channels:
        potential_channel = get_channel(channel_id)

        try:
            message = potential_channel.get_message(message_id)
            channel = potential_channel
            break
        except Value_Error:
            continue

    if message is None:
        raise Value_Error(description="Message does not exist")

    if channel is None:
        raise Value_Error(description="Channel does not exist")

    if not user.is_global_admin() and not is_user_owner(u_id, channel.get_id()):
        raise Value_Error(description="Only admins and owners can unpin messages!")

    if not message.is_pinned():
        raise Value_Error(description="The message is not pinned")

    # otherwise unpin the message and remove it from the channel's
    # list of pins
    message.set_pinned(False)
    channel.remove_pin(message_id)

    return {}


def message_react(token, message_id, react_id):
    channels = get_data()["channels"]

    u_id = check_valid_token(token)

    message = None
    for channel_id in channels:
        channel = get_channel(channel_id)

        try:
            message = channel.get_message(message_id)
            break
        except Value_Error:
            continue

    if message is None:
        raise Value_Error(description="Message does not exist")

    react_exists = False
    for react in message.get_reacts():
        if react["react_id"] == react_id:
            if u_id in react["u_ids"]:
                raise Value_Error(description=f"You have already reacted to\
                                  this message with this react")
            react_exists = True
            react["u_ids"].append(u_id)
            break

    if not react_exists:
        message.get_reacts().append({
            "react_id" : react_id,
            "u_ids" : [u_id]
        })

    return {}


def message_unreact(token, message_id, react_id):
    channels = get_data()["channels"]

    u_id = check_valid_token(token)

    message = None
    for channel_id in channels:
        channel = get_channel(channel_id)

        try:
            message = channel.get_message(message_id)
            break
        except Value_Error:
            continue

    if message is None:
        raise Value_Error(description="Message does not exist")

    for react in message.get_reacts():
        if react["react_id"] == react_id:
            if u_id not in react["u_ids"]:
                raise Value_Error(description="You have not reacted to this\
                                  message with this react")
            react["u_ids"].remove(u_id)
            break

    return {}

def search(token, query_str):
    """
    search(token, query_str);
    return {messages}
    Exception: N/A
    Description: Given a query string, return a collection of messages that match the query
    """
    # call the database
    server_data = get_data()

    # check if the token is valid and decode it
    u_id = check_valid_token(token)

    # suppress pylint error
    assert u_id is not None

    # initialise an empty list
    message_match = []

    for channel_id in get_data()["channels"]:
        # check that the user has access to this channel
        if not is_user_member(u_id, channel_id) and not \
           (user.is_global_admin() or user.is_slackr_owner()):
            continue

        channel = get_channel(channel_id)

        for message in channel.get_messages():
            if query_str in message:
                message_match.append(message)

    return message_match
