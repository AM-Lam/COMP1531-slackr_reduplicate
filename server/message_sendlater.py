from .channels_listall import channels_listall
from datetime import datetime


def message_sendlater(token, channel_id, message, time_sent):
    # first deal with an easy to catch error, is the message too large to send
    if len(message) > 1000:
        raise ValueError("Messages must be below 1000 characters")
    
    # next error, check the current date against time_sent and raise an
    # exception if time_sent is in the past
    if datetime.now() > time_sent:
        raise ValueError("Cannot send messages in the past")
        
    # ensure that the channel we are trying to send a message to actually exists
    # and that we are an authorised user in it (which I take here to mean a
    # member of the channel)
    channel_exists = False
    for channel in channels_listall(token):
        if channel_id == channel["channel_id"]:
            # check whether or not the user is authorised to send messages in
            # this channel, I presume we will need to access a database to do
            # this
            channel_exists = True
            break
    
    if not channel_exists:
        raise ValueError("Channel does not exist")
    
    # now send the message with the time_created being time_sent to the server
    # this will require access to the database and server so we can't really
    # do anything with it right now, see assumptions.md for why I'm doing it
    # this way rather than using threading or something similar
    
    return {}

