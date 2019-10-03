import setup
from setup import AccessError

token = setup.generateToken('hayden@gmail.com', '123456', 'Hayden', 'Smith')
channel_id = setup.generateChannel(token, "Channel 1", True)
messageId = "456789"

def message_send(token, channel_id, message):
    # ValueError when:Message is more than 1000 characters
    if (len(message) > 1000):
        raise ValueError("The message is too long. Please keep it within 1000 characters.")   


def message_remove(token, message_id):
    # ValueError when:Message (based on ID) no longer exists
    if message_id == None:
        raise ValueError("The message is no longer exists")
        pass

    # AccessError: Message with message_id was not sent by the authorised user making this request

    # AccessError: Message with message_id was not sent by an owner of this channel
    
    # AccessError: Message with message_id was not sent by an admin or owner of the slack



def message_edit(token, message_id, message):
    pass