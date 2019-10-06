import pytest
import message_(un)pin

def test_message_pin(token, message_id):
    # assert message_pin(token, message_id) == None
    
    assert message_pin('456','message') == None
    
    with pytest.raise(ValueError)
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_pin('123','message__')
    #  The authorised user is not an admin
        message_pin('123','id')
        message_pin('123','message_id')
    #  Message with ID message_id is already pinned
    def double_pin():
        message_pin('456','message')
        with pytest.raise(ValueError):
            message_pin('456','message')

    with pytest.raises(AccessError): 
    #  The authorised user is not a member of the channel that the message is within
        message_pin('456','id')
    
    
def test_message_unpin(token, message_id):
    assert message_unpin(token, message_id) == None
    
    with pytest.raise(ValueError)
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_unpin('123','message__')
    #  The authorised user is not an admin
        message_unpin('123','id')
        message_unpin('123','message_id')
    #  Message with ID message_id is already unpinned
    def double_pin():
        message_pin('456','message')
        message_unpin('456','message')
        with pytest.raise(ValueError):
            message_unpin('456','message')

    with pytest.raises(AccessError): 
    #  The authorised user is not a member of the channel that the message is within
        message_unpin('456','id')
    