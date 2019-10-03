import setup

token = setup.generateToken('hayden@gmail.com', '123456', 'Hayden', 'Smith')
channel_id = setup.generateChannel(token, "Channel 1", True)
message_id = setup.generateMessage(token, channel_id, message)
permission_id = "admin"

def message_pin(token, message_id):
    pass
    
    
def message_unpin(token, message_id):
    pass
