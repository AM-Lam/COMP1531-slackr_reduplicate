import pytest
import message_(un)react

def test_message_react():
    #assert message_react(token, message_id, react_id) == None
    assert message_react('person2', 3, 1) == None
    assert message_react('person2', 4, 2) == None
    assert message_react('person3', 3, 3) == None
    assert message_react('admin2', 4, 4) == None

    # Poster reacts on their own message
    assert message_react('person1', 1, 1) == None
    assert message_react('admin1', 1, 4) == None

    with pytest.raise(ValueError):
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_react('person1', 45, 1)
        message_react('admin2', 78, 1)
        message_react('owner', 16, 3)

    #  react_id is not a valid react ID
        message_react('person1', 5, 47)
        message_react('person2', 4, 46) 

    #  Message with ID message_id already contains an active React with ID react_id
        message_react('owner',1, 4)
        message_react('person3', 2, 1)
    
def test_message_unreact():
    # assert message_unreact(token, message_id, react_id) == None
    assert message_unreact('person1',1,2) == None
    assert message_unreact('person1',1,2) == None

    def test_basic_case():
        message_react('admin2', 4, 4)
        assert message_unreact('admin2', 4 , 4) == None

    with pytest.raise(ValueError): 
    #  message_id is not a valid message within a channel that the authorised user has joined
        message_unreact('person1', 88, 1)
        message_unreact('person3', 45, 1)
        message_unreact('admin1', 78, 1)

    #  react_id is not a valid React ID
        message_unreact('person3', 3, 18)
        message_unreact('admin2', 3, 28) 

    #  Message with ID message_id already contains an active React with ID react_id
    def test_double_unreact():
        message_react('person2', 3, 3)
        message_unreact('person1', 1, 3)
        with pytest.raises(ValueError):
            message_unreact('person1', 1, 3)
