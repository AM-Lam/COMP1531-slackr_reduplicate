def test_message_send(token, channel_id, message):
    assert message_send(token, channel_id, message) == []
    # ValueError when:Message is more than 1000 characters