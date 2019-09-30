def test_message_edit(token, message_id, react_id):
    assert message_send(token, message_id, react_id) == []
    # ValueError when:
    #  message_id is not a valid message within a channel that the authorised user has joined
    #  react_id is not a valid React ID
    #  Message with ID message_id already contains an active React with ID react_id