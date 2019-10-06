import pytest

def test_message_edit():
    assert message_edit('person1', 1, 'hello') == None
    assert message_edit('person1', 2, 'he ll.;...,o JHBF65154') == None
    assert message_edit('person2', 4, 'KJENF39482UEhUr8u309rqj') == None
    assert message_edit('admin1', 5, 'GKREgW2twKzcZ9wMe3zMsl0yf8OJfYOAB9I9DWd81pIPRmlq7v1p5j1tfifWu8kcoXkG1wu0qLK7xfhHlJUg12Yxr') == None

    # if user is not a member of a certain channel anymore
    def test_error_leave_channel():
        channel_leave('person1', 1)
        with pytest.raises(AccessError) :
            message_edit('person1', 1)

    def test_not_the_user():
        message_send('person1', 8, 'hello')
        with pytest.raises(ValueError):
            #  Message with message_id edited by authorised user is not the poster of the message
            message_edit('person3', 8, 'FakeHello')

    # user not the poster
    with pytest.raises(ValueError):
        message_edit('person3', 1, 'RealHello?')

    #  Message with message_id is not a valid message
    #     1) is a message sent by the authorised user
    # The message is over 1000 characters
        message_edit('person1', 1, 'bfiDw25miCyBvrwSfYWVRTSdunVfTxzWRfkYrvOztvF3BrtCHbXWoIKPbpBhYdQsWf7TTWQ5Z0cKmBBygwVRAyS9Yt6YBtitWYQDVVVembsy7izJMjuVk611l7NmxPWXw8w8pk7EtKHq1464icy6z5qcnG6cSALJUT86hU2tXG3redpcINHEG9BaNTqgngUSGNENIVkD9mzYRFeChjq7CBwZVP7G0yCYxn3M3VSgUIyFbQElRGkKtX7KWvg9FxlFXnld8ScXaTE27i8zT4FqZMf8j45wVYZOJLRpOnX1JaDvfvpMfG5ybCleIQYe9GADEzcP7RxBcs7EaIqSRmpXOZl3kyJDdYubEttcR9rrulQo3dJMzPa3WnaosCByZCEeO3rqHqryXcpwlB8Z5ztYGJ8fiRDMgwloBjjAZyHPU6CTd76zFRXPyywnjzQhmsBVHQ6qjyNQODV9j2mLejkCVjFXgVYbOfQnSQZALo7PDkB4BEQDJWY4GVtG7FfhhGM9YsolHDWzQnGkFjvPfLgI1rXNsacFr2jbb5qv7C8nCnE63BDroyI0UjR0iQqFuNIuJI2pxuibdxZcsifRFjhf3j86Ya03mSBBxoULl8o9mOZx60nYalsQcBGd56qavrrLIqxWB6KOhLoFhSwOyZCc4bU3s4UX8oN0s9BXaeAM7S6dyLbI8qA6OKJFHmpUielq6dlaaSXHOZMmOgG5K6lmpUvaxc9vz0AUmgWTo8ENHv1iHFoqEDgWsjbziBkRaxxCCnyoE6qg00OvNxerVNLQgEYYVj9TBeEPbXlDCQSvx50RAEbE8PxRsf9Fp0ZvdqXcyOr3ZtZ6X20afRnkZx8bcll7UF7LKBJl3BFrRGcpKoT5rUpAEifG3tMNB1jANgrJSbdkh4fwkCRfX1n52VyO9xnXTqijFmr1zMg01SpuSRTcqu901OA4kOQZzh0iQk1baCQDEOrFtDSuSLtXTYXl6nS5upAK0v8AnRxtlsdflhyge')
    #     2) If the authorised user is an admin, is a any message within a channel that the authorised user has joined
        message_edit('admin1', 1, 'lo')
        message_edit('admin2', 2, 'NOt')
