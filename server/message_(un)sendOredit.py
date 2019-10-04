import setup
from setup import AccessError
# TODO
# Have to include the related file name later
from channel_details.file import channel_details

token = setup.generate_token('hayden@gmail.com', '123456', 'Hayden', 'Smith')
channel_id = setup.generate_channel(token, "Channel 1", True)
channel_id_list = {'channel 1', 'Channel 1', 'channel1'}
message_id = "456789"
# format of message_id_dic: 'message_id':{'token', 'channel_id'}
message_id_dic = {'message_id': {'123', 'channel1'}, 'message': {'456', 'channel 1'}, 'id': {'123', 'Channel 1'}}
permission_id = {'123': 'member' ,'456': 'admin', '789': 'member', 'AD': 'admin', '159':'owner'}

# for all the message_id, i am using a dictionary to store the message_id as key and token as value

def message_send(token, channel_id, message):
    # Message is more than 1000 characters
    if (len(message) > 1000):
        raise ValueError("The message is too long. Please keep it within 1000 characters.")   

    # generate message id and store it in dictionary if it is succeeded
    setup.generate_message_id()

def message_remove(token, message_id):
    # Message (based on ID) no longer exists
    # or the message Id never exists
    if message_id == None:
        raise ValueError("The message is not existing. Please try again")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    if message_id_dic[message_id][0] != token:
        raise AccessError("You have no permission to remove the message. Messages can only be deleted by sender or admin.")

    token_of_message = message_id_dic[message_id][0]
    # if channel_details succeed, it should return None
    if channel_details(token_of_message, message_id_dic[message_id][1]) != None:
        if permission_id[token_of_message] == 'member':  
            #  Person who make the request is not an admin or owner in the channel so they don't have permission to remove the message
            raise AccessError("You don't have access to remove the message. Only the sender or admin shall make this request.")
        else: 
            # Since it also fail the channel_details so something must be wrong with the token or channel
            raise AccessError("Invalid")
    
    #If the function is successfully executed
    del message_id_dic[message_id]


def message_edit(token, message_id, message):
    # basic case
    # if the message_id cannot be found
    if message_id == None:
        raise ValueError("The message is not existing. Please try again.")

    # ValueError when:
    #  Message with message_id edited by authorised user is not the poster of the message
    token_of_message = message_id_dic[message_id][0]
    if token_of_message != token:
        raise ValueError("As a user, you have no permission to remove the message.")
    #  Message with message_id is not a valid message
    if permission[message_id_dic[message_id][0]] == member:
    #     1) is a message sent by the authorised user
    # message doesn't have the right format or character limitation. E
    # Even though it is sent by the right person the request is still denied
        if (len(message) > 1000):
            raise ValueError("The message is too long. Please keep it within 1000 characters.")   
    #     2) If the authorised user is an admin, is a any message within a channel that the authorised user has joined
    else:
        raise ValueError("Only writer of the message have the permission to edit the message")   

    # if the function is executed, i suppose this is the way to change the message's content
    message_id_dic['token'] = message
