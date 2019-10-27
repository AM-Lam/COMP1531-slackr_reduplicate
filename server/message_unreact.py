import jwt
from .database import *
from .access_error import *


def message_unreact(token, message_id, react_id):
    server_data = get_data()

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, True):
        raise AccessError(description="This token is invalid")

    # Message with message_id was not sent by the authorised user making this request
    # person who send this message is not the sender and not an admin or owner in the channel
    channel_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id:
                channel_ = channel
                break
    
    if channel_ is None:
        raise ValueError(description="Channel does not exist")

    obj_request = None
    for user in server_data["users"]:
        if user.get_u_id() == u_id:
            obj_request = user
            break

    user_id = obj_request.get_u_id()

    # the message is not existed
    if user_id is None:
        raise AccessError(description="The message is not existed")

    # if user is not the poster
    if u_id != user_id:
        raise AccessError(description="You don't have access to delete")

    react_id = 1
    if u_id not in obj_request._reacts['u_id']:
        raise AccessError("Invalid unreact")

    if obj_request._reacts['is_this_user_reacted'] == False:
        raise ValueError(description="Invalid unreact")
    else:
        for item in obj_request._reacts:
            if item['u_id'] == u_id:
                item['is_this_user_reacted'] = False
                del item
            else:
                raise AccessError(description="Invalid unreact")

