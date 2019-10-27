import pytest
import jwt
from .access_error import *
from .database import *
from .channel_leave import channel_leave
from .message_unpin import message_unpin
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove
from .message_pin import message_pin


def test_message_unpin():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None
    message_pin(user1["token"], message_1['message_id']) 

    assert message_unpin(user1["token"], message_1['message_id']) == {}


def test_no_message():
    clear_data()
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to remove a non-existent message
    pytest.raises(ValueError, message_unpin, user1["token"], 123)

# def test_message_unpin():
#     #assert message_unpin(token, message_id) == None
#     assert message_unpin('admin1', 1) == None
#     assert message_unpin('owner', 5) == None

#     def test_basic_case():
#         message_pin('owner', 3)
#         message_unpin('owner', 3)
    
#     with pytest.raises(ValueError):
#     #  message_id is not a valid message within a channel that the authorised user has joined
#         message_unpin('admin1', 78)
#     #  The authorised user is not an admin
#         message_unpin('person1', 1)
#         message_unpin('person2', 3)
#         message_unpin('person3', 1)
#         message_unpin('person3', 2)

#     #  Message with ID message_id is already unpinned
#     def double_unpin():
#         message_pin('admin2', 1)
#         message_unpin('admin2', 1)
#         with pytest.raises(ValueError):
#             message_unpin('admin2', 1)

#     #  The authorised user is not a member of the channel that the message is within
#     def test_error_leave_channel():
#         message_pin('admin1', 1)
#         channel_leave('admin1', 1)
#         with pytest.raises(AccessError) :
#             message_unpin('admin1', 1)
    
