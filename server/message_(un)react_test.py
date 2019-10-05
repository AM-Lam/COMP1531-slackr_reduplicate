import pytest
import message_(un)react

def test_message_react(token, message_id, react_id):
    assert message_react(token, message_id, react_id) == None
    assert message_react('123', 'id', 'sad') == None

    with pytest.raise(ValueError):
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_react('123','message', 'angry')

    #  react_id is not a valid React ID
        message_react('123', 'id', 'bad')
        message_react('123', 'id', 'smiie') #typo there

    #  Message with ID message_id already contains an active React with ID react_id
        message_react('123','message_id', 'smile')
        message_react('456','message', 'angry')
    
def test_message_unreact(token, message_id, react_id):
    assert message_unreact(token, message_id, react_id) == None
    assert message_unreact('123','message_id','like') == None

    with pytest.raise(ValueError): 
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_unreact('123','message', 'angry')

    #  react_id is not a valid React ID
        message_unreact('123', 'id', 'bad')
        message_unreact('123', 'id', 'smiie') #typo there
    #  Message with ID message_id already contains an active React with ID react_id
        message_unreact('123','message_id', 'smile')
        message_unreact('456','message', 'angry')
