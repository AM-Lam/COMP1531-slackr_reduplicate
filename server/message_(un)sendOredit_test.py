def test_message_send(token, channel_id, message):
    assert message_send(token, channel_id, message) == []
    # ValueError when:Message is more than 1000 characters
    
    
def test_message_remove(token, message_id):
    assert message_remove(token, message_id) == []
    # ValueError when:Message (based on ID) no longer exists
    # AccessError whenUser does not have permission to remove that row


def test_message_edit(token, message_id, message):
    assert message_edit(token, message_id, message) == []
    # ValueError when:
    #  Message with message_id edited by authorised user is not the poster of the message
    #  Message with message_ is not a valid message that either 
    #  1) is a message sent by the authorised user, or; 
    #  2) If the authorised user is an admin, is a any message within a channel that the authorised user has joined
