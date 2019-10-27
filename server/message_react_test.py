import pytest
import re
import jwt
from .database import *
from .access_error import *
from .message_react import message_react
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove


def test_message_react():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    react_id = 1
    assert message_react(user1["token"], message_1['message_id'], react_id) == {}
                        

def test_no_message():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    message_remove(user1["token"], message_1['message_id'])

    react_id = 1
    # the message is not existed
    pytest.raises(ValueError, message_react, user1["token"], message_1['message_id'], react_id)

# def test_message_react():
#     #assert message_react(token, message_id, react_id) == None
#     assert message_react('person2', 3, 1) == None
#     assert message_react('person2', 4, 2) == None
#     assert message_react('person3', 3, 3) == None
#     assert message_react('admin2', 4, 4) == None

#     # Poster reacts on their own message
#     assert message_react('person1', 1, 1) == None
#     assert message_react('admin1', 1, 4) == None

#     with pytest.raises(ValueError, r"*"):
#     #  message_id is not a valid message within a channel that the authorised user has joined
#         message_react('person1', 45, 1)
#         message_react('admin2', 78, 1)
#         message_react('owner', 16, 3)

#     #  react_id is not a valid react ID
#         message_react('person1', 5, 47)
#         message_react('person2', 4, 46) 

#     #  Message with ID message_id already contains an active React with ID react_id
#         message_react('owner',1, 4)
#         message_react('person3', 2, 1)
