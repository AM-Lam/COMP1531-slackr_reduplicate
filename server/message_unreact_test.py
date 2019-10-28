import pytest
import jwt
from .access_error import *
from .database import *
from .message_unreact import message_unreact
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove
from .message_react import message_react


def test_message_unreact():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    react_id = 1
    message_react(user1["token"], message_1['message_id'], react_id)
                        
    assert message_unreact(user1["token"], message_1['message_id'], react_id) == {}


def test_no_message():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")
    message_remove(user1["token"], message_1['message_id'])

    react_id = 1
    
    # message is not existed
    assert message_1 is None
    # the message is not existed
    pytest.raises(ValueError, message_unreact, user1["token"], message_1['message_id'], react_id)


# def test_message_unreact():
#     # assert message_unreact(token, message_id, react_id) == None
#     assert message_unreact('person1',1,2) == None
#     assert message_unreact('person1',1,2) == None

#     def test_basic_case():
#         message_react('admin2', 4, 4)
#         assert message_unreact('admin2', 4 , 4) == None

#     with pytest.raises(ValueError): 
#     #  message_id is not a valid message within a channel that the authorised user has joined
#         message_unreact('person1', 88, 1)
#         message_unreact('person3', 45, 1)
#         message_unreact('admin1', 78, 1)

#     #  react_id is not a valid React ID
#         message_unreact('person3', 3, 18)
#         message_unreact('admin2', 3, 28) 

#     #  Message with ID message_id already contains an active React with ID react_id
#     def test_double_unreact():
#         message_react('person2', 3, 3)
#         message_unreact('person1', 1, 3)
#         with pytest.raises(ValueError):
#             message_unreact('person1', 1, 3)
