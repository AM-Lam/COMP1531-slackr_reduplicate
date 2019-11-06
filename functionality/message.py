import threading
from datetime import datetime
import jwt
from .database import check_valid_token, get_data, get_secret, Messages
from .access_error import AccessError, Value_Error


def send_message(channel, message, time_sent):
    # wait until we have passed beyond the desired time to send the message
    while datetime.utcnow() < time_sent:
        continue
    
    # now just append the message we created earlier to the provided channel
    channel.add_message(message)


def message_send(token, channel_id, message):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]
    
    # Message is more than 1000 characters
    if len(message) > 1000:
        raise Value_Error(description="Messages must be less than 1000 characters")

    channel_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        if channel.get_id() == channel_id:
            channel_ = channel
            break
    
    if channel_ is None:
        raise Value_Error(description="Channel does not exist")

    if u_id not in channel_.get_members():
        raise AccessError(description="You don't have access in this channel")
        
    # now create the message we will be sending
    message_id = channel_.get_m_id()
    to_send = Messages(message_id, u_id, message, channel_id,
                       datetime.utcnow(), [])
    
    # increment the channel's max message id
    channel_.increment_m_id()
    
    send_message(channel_, to_send, datetime.utcnow())

    # return the new message's id
    return {"message_id" : message_id}


def message_sendlater(token, channel_id, message, time_sent):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # first deal with an easy to catch error, is the message too large to send
    if len(message) > 1000:
        raise Value_Error(description="Messages must be below 1000 characters")
    
    # next error, check the current date against time_sent and raise an
    # exception if time_sent is in the past
    if datetime.utcnow() > time_sent:
        raise Value_Error(description="Cannot send messages in the past")
        
    # ensure that the channel we are trying to send a message to actually exists
    # and that we are an authorised user in it (which I take here to mean a
    # member of the channel)
    channel_ = None
    for channel in server_data["channels"]:
        if channel_id == channel.get_id():
            channel_ = channel
            break
    
    if channel_ is None:
        raise Value_Error(description="Channel does not exist")
    
    if u_id not in channel_.get_members():
        raise AccessError(description="You cannot send messages in this channel")
    
    # now create the message we will be sending
    m_id = channel_.get_m_id()
    to_send = Messages(m_id, u_id, message, channel_id,
                       time_sent, [])
    
    # increment the channel's max message id
    channel_.increment_m_id()
    
    # start a thread that will call send_message
    threading.Thread(target=send_message, args=(channel_, to_send, time_sent)).start()
    
    return {"message_id" : m_id}


def message_edit(token, message_id, message):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]
    
    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # Message is more than 1000 characters
    if len(message) > 1000:
        raise Value_Error(description="Messages must be less than 1000 characters")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    message_ = None
    channel_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for m in channel.get_messages():
            if m.get_m_id() == message_id:
                channel_ = channel
                message_ = m
                break
    
    if message_ is None:
        raise Value_Error(description="Message does not exist")

    user_ = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            if (message_.get_u_id() != u_id and not user.is_global_admin()
                and not u_id in channel_.get_owners()):
                break
            user_ = user
            break

    # if user is not the poster or admin
    if user_ is None:
        raise AccessError(description="You do not have permission to edit this message")
    
    print(f'Message object {message_} has text {message_.get_text()}')
    # update the database with new message
    message_.edit_text(message)
    print(f'Message object {message_} has text {message_.get_text()}')
            
    return {}


def message_remove(token, message_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    message_ = None
    
    # check if this channel
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id:
                message_ = message
                break
    
    if message_ is None:
        raise Value_Error(description="Message does not exist")

    user_ = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            if user.get_u_id() != message_.get_u_id() and not user.is_global_admin():
                break
            user_ = user
            break

    if user_ == None:
        # if user is not the poster or an admin
        raise AccessError(description="You don't have access to delete")
    
    # remove the message to the server database
    channel._messages.remove(message)

    return {}


def message_pin(token, message_id):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # make sure the user is an admin
    user_ = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            user_ = user
            break
    
    if user_ == None:
        raise Value_Error("u_id does not belong to a real user")
    
    # Message with message_id was not sent by the authorised user making this
    # request person who send this message is not the sender and not an admin
    # or owner in the channel
    channel_ = None
    message_ = None
    
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id:
                channel_ = channel
                message_ = message
                break
    
    if message_ is None:
        raise Value_Error(description="The provided id does not refer to a real message")
    
    if user_.is_global_admin() == False and u_id not in channel_.get_owners():
        raise Value_Error(description="Only admins and owners can pin messages!")
    #  Message with ID message_id is already pinned
    if message_._pinned == True:
        raise Value_Error(description="The message is already pinned")
    else:
        # pin the message and add it to the channels list of pins
        message_._pinned = True
        print(message_._pinned)
        channel_.add_pin(message_.get_m_id())

    return {}


def message_unpin(token, message_id):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    channel_ = None
    message_ = None
    
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id:
                channel_ = channel
                message_ = message
                break

    user_ = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            user_ = user
            break
    
    if user_ == None:
        raise Value_Error("u_id does not belong to a real user")

    if message_ is None:
        raise Value_Error(description="The provided id does not\
                         refer to a real message")
    
    if user_.is_global_admin() == False and u_id not in channel_.get_owners():
        raise Value_Error(description="Only admins and owners can unpin\
                         messages!")
    #  Message with ID message_id is already pinned
    if message_._pinned == False:
        raise Value_Error(description="The message is not pinned")
    else:
        # pin the message and add it to the channels list of pins
        message_._pinned = False
        channel_._pinned_messages.remove(message_.get_m_id())
    
    return {}


def message_react(token, message_id, react_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    message_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id and u_id in channel.get_members():
                message_ = message
                break
    
    if message_ is None:
        raise Value_Error(description="Message does not exist")

    react_exists = False
    for react in message_._reacts:
        if react["react_id"] == react_id:
            if u_id in react["u_ids"]:
                raise Value_Error(description=f"You have already reacted to this message with this react")
            react_exists = True
            react["u_ids"].append(u_id)
            break
    
    if not react_exists:
        message_._reacts.append({
            "react_id" : react_id,
            "u_ids" : [u_id]
        })

    return {}


def message_unreact(token, message_id, react_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, False):
        raise AccessError(description="This token is invalid")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    message_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id and u_id in channel.get_members():
                message_ = message
                break
    
    if message_ is None:
        raise Value_Error(description="Message does not exist")

    for react in message_._reacts:
        if react["react_id"] == react_id:
            if u_id not in react["u_ids"]:
                raise Value_Error(description=f"You have not reacted to this message with this react")
            react["u_ids"].remove(u_id)
            break

    return {}

def search(token, query_str):
    # find u_id associated with token (with non-existent database)
    DATABASE = get_data()
    admin_user_id = check_valid_token(token)

    # suppress pylint error
    assert admin_user_id is not None

    # pull messages from a list/dictionary of all messages
    message_match = []
    
    # TODO: write check for if user has access to channel
    for channel in DATABASE["channels"]:
        for message in channel.get_messages():
            if query_str in message:
                message_match.append(message)

    return message_match
