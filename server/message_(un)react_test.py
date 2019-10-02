import pytest
import message_(un)react

def test_message_react(token, message_id, react_id):
    assert message_react(token, message_id, react_id) == []
    # ValueError when:
    #  message_id is not a valid message within a channel that the authorised user has joined
    #  react_id is not a valid React ID
    #  Message with ID message_id already contains an active React with ID react_id
    
def test_message_unreact(token, message_id, react_id):
    assert message_unreact(token, message_id, react_id) == []
    # ValueError when:
    #  message_id is not a valid message within a channel that the authorised user has joined
    #  react_id is not a valid React ID
    #  Message with ID message_id does not contain an active React with ID react_id
