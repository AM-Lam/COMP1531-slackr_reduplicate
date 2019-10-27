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
    message_ = None
    # add the message to the server database
    for channel in server_data["channels"]:
        for message in channel._messages:
            if message.get_m_id() == message_id and u_id in channel.get_members():
                message_ = message
                break
    
    if message_ is None:
        raise ValueError(description="Message does not exist")

    for react in message_._reacts:
        if react["react_id"] == react_id:
            if u_id not in react["u_ids"]:
                raise ValueError(description=f"You have not reacted to this message with this react")
            react["u_ids"].remove(u_id)
            break

    return {}