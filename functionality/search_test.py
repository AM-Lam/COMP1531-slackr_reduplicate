import pytest
from .search import search
from .auth import auth_register
from .database import clear_data
from .access_error import *

def test_search():
    clear_data()
    
    user1 = auth_register("valid@email.com", "1234567890", "John", "Doe")
    user2 = auth_register("valid2@email.com", "0123456789", "John", "Bobs")

    # public channel for testing
    channel_id = channels_create(user1["token"], "Channel 1", True)
    # private channel for testing
    channel_id = channels_create(user2["token"], "Channel 2", False)

    # try to create a valid message
    message_1 = message_send(user1["token"], "Channel 1", "hewwo dere")
    # try to create a message in a private chat
    message_2 = message_send(user2["token"], "Channel 2", "uwu whats this")

    # find all the matching messages
    assert search(user1["token"], "hewwo") == {"messages": [message_1]}

    # user1 does not have access so they can't access the messages
    assert search(user1["token"], "uwu") == {}

    # but user2 can access those messages
    assert search(user2["token"], "uwu") == {"messages": [message_2]}

    # return nothing if the query string is nothing
    assert search(user1["token"], "") == {}

    # if query string is a space, return almost anything
    assert search(user2["token"], " ") == {"messages": [message_1, message_2]}
