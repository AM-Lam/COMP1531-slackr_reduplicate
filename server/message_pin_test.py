def test_message_pin(token, message_id):
    assert message_unreact(token, message_id) == []
    # ValueError when:
    #  message_id is not a valid message within a channel that the authorised user has joined
    #  The authorised user is not an admin
    #  Message with ID message_id is already pinned
    # AccessError when:
    #  The authorised user is not a member of the channel that the message is within