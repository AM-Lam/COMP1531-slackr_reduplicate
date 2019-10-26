import pytest
import jwt
from .access_error import *
from .database import *
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .message_remove import message_remove
from .message_edit import message_edit

clear_data()

def verify_message(message_obj, correct_data):
    if message_obj == correct_data:
        return True
    return False

def test_message_edit():
    user1 = auth_register("valid@email.com", "123465", "Bob", "Jones")

    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the message exists
    assert message_1 is not None

    message_remove(user1["token"], message_1['message_id'])

    # check that the channel exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert message_edit(user1["token"], message_1['message_id'], "Hi") == None
    
# def test_no_message():
    
#     # just got the u_id by putting fake data into jwt.io
#     secret = get_secret()
#     user1 = {
#         "token" : jwt.encode({"u_id" : "111"}, secret, algorithm="HS256").decode(),
#         "u_id" : "111"
#     }

#     user2 = {
#         "token" : jwt.encode({"u_id" : "22"}, secret, algorithm="HS256").decode(),
#         "u_id" : "22"
#     }

#     user3 = {
#         "token" : jwt.encode({"u_id" : "3"}, secret, algorithm="HS256").decode(),
#         "u_id" : "3"
#     }
    
#     channel_id = channels_create(user1["token"], "Channel 1", True)

#     # try to create a valid message
#     message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

#     # check that the channel exists
#     assert message_1 is not None

#     message_remove(user1["token"], message_1['message_id'])

#     # message is not existed
#     assert message_1 is None
#     # the message is not existed
#     pytest.raises(ValueError, message_edit, user1["token"], message_1['message_id'], "hi")

# def test_invalid_user_admin():
    # user1 = auth_register("valid@email.com", "1234", "Bob", "Jones")

    # just got the u_id by putting fake data into jwt.io
    # secret = get_secret()
    # user1 = {
    #     "token" : jwt.encode({"u_id" : "111"}, secret, algorithm="HS256").decode(),
    #     "u_id" : "111"
    # }

    # user2 = {
    #     "token" : jwt.encode({"u_id" : "22"}, secret, algorithm="HS256").decode(),
    #     "u_id" : "22"
    # }

    # user3 = {
    #     "token" : jwt.encode({"u_id" : "3"}, secret, algorithm="HS256").decode(),
    #     "u_id" : "3"
    # }
    
    # channel_id = channels_create(user1["token"], "Channel 1", True)

    # # try to create a valid message
    # message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # # check that the channel exists
    # assert message_1 is not None

    # pytest.raises(AccessError, message_edit, user3["token"], message_1['message_id'], "hi")


# def test_message_edit():
#     assert message_edit('person1', 1, 'hello') == None
#     assert message_edit('person1', 2, 'he ll.;...,o JHBF65154') == None
#     assert message_edit('person2', 4, 'KJENF39482UEhUr8u309rqj') == None
#     assert message_edit('admin1', 5, 'GKREgW2twKzcZ9wMe3zMsl0yf8OJfYOAB9I9DWd81pIPRmlq7v1p5j1tfifWu8kcoXkG1wu0qLK7xfhHlJUg12Yxr') == None

#     # if user is not a member of a certain channel anymore
#     def test_error_leave_channel():
#         channel_leave('person1', 1)
#         with pytest.raises(AccessError) :
#             message_edit('person1', 1)

#     def test_not_the_user():
#         message_send('person1', 8, 'hello')
#         with pytest.raises(ValueError):
#             #  Message with message_id edited by authorised user is not the poster of the message
#             message_edit('person3', 8, 'FakeHello')

#     # user not the poster
#     with pytest.raises(ValueError):
#         message_edit('person3', 1, 'RealHello?')

#     #  Message with message_id is not a valid message
#     #     1) is a message sent by the authorised user
#     # The message is over 1000 characters
#         message_edit('person1', 1, 'bfiDw25miCyBvrwSfYWVRTSdunVfTxzWRfkYrvOztvF3BrtCHbXWoIKPbpBhYdQsWf7TTWQ5Z0cKmBBygwVRAyS9Yt6YBtitWYQDVVVembsy7izJMjuVk611l7NmxPWXw8w8pk7EtKHq1464icy6z5qcnG6cSALJUT86hU2tXG3redpcINHEG9BaNTqgngUSGNENIVkD9mzYRFeChjq7CBwZVP7G0yCYxn3M3VSgUIyFbQElRGkKtX7KWvg9FxlFXnld8ScXaTE27i8zT4FqZMf8j45wVYZOJLRpOnX1JaDvfvpMfG5ybCleIQYe9GADEzcP7RxBcs7EaIqSRmpXOZl3kyJDdYubEttcR9rrulQo3dJMzPa3WnaosCByZCEeO3rqHqryXcpwlB8Z5ztYGJ8fiRDMgwloBjjAZyHPU6CTd76zFRXPyywnjzQhmsBVHQ6qjyNQODV9j2mLejkCVjFXgVYbOfQnSQZALo7PDkB4BEQDJWY4GVtG7FfhhGM9YsolHDWzQnGkFjvPfLgI1rXNsacFr2jbb5qv7C8nCnE63BDroyI0UjR0iQqFuNIuJI2pxuibdxZcsifRFjhf3j86Ya03mSBBxoULl8o9mOZx60nYalsQcBGd56qavrrLIqxWB6KOhLoFhSwOyZCc4bU3s4UX8oN0s9BXaeAM7S6dyLbI8qA6OKJFHmpUielq6dlaaSXHOZMmOgG5K6lmpUvaxc9vz0AUmgWTo8ENHv1iHFoqEDgWsjbziBkRaxxCCnyoE6qg00OvNxerVNLQgEYYVj9TBeEPbXlDCQSvx50RAEbE8PxRsf9Fp0ZvdqXcyOr3ZtZ6X20afRnkZx8bcll7UF7LKBJl3BFrRGcpKoT5rUpAEifG3tMNB1jANgrJSbdkh4fwkCRfX1n52VyO9xnXTqijFmr1zMg01SpuSRTcqu901OA4kOQZzh0iQk1baCQDEOrFtDSuSLtXTYXl6nS5upAK0v8AnRxtlsdflhyge')
#     #     2) If the authorised user is an admin, is a any message within a channel that the authorised user has joined
#         message_edit('admin1', 1, 'lo')
#         message_edit('admin2', 2, 'NOt')
