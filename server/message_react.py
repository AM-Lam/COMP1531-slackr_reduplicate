import jwt
import threading
from .database import *
from .access_error import *

def message_react(token, message_id, react_id):
    server_data = get_data()

    # if the token is not valid raise an AccessError
    if not server_data["tokens"].get(token, True):
        raise AccessError(description="This token is invalid")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # Message (based on ID) no longer exists
    # or the message Id never exists
    if message_id not in server_data['channels']._messages:
        raise ValueError #("The message is not existing. Please try again")

    for channel in server_data['channels']:
        for message in channel._messages:
            # the message is not existed
            # double check
            if message_id not in message._message_id:
                raise AccessError 
            else:
                if u_id in channels_list(token):
                    # user can only react to same message once
                    if u_id not in message.message_react:
                        message.message_react.append(
                            { 
                                'react_id': react_id,
                                'u_id': u_id,
                                'is_this_user_reacted': True
                            }
                        )
                    else:
                        for this_u_id in message.message_react:
                            if this_u_id == u_id:
                                if this_u_id['is_this_user_reacted'] == True:
                                    raise ValueError 
                                else:
                                    # update react
                                    this_u_id['react_id'] = react_id
                                    this_u_id['is_this_user_reacted'] = True
