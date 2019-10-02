def test_message_remove(token, message_id):
    assert message_send(token, message_id) == []
    # ValueError when:Message (based on ID) no longer exists
    # AccessError whenUser does not have permission to remove that row