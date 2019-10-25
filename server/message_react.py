#from .database import *
import jwt
# from .access_error import AccessError
import access_error
# from .channels_list import channels_list
import channels_list

def message_react(token, message_id, react_id):
    server_data = get_data()

    # Message (based on ID) no longer exists
    # or the message Id never exists
    if message_id not in server_data['channels']._messages:
        raise ValueError #("The message is not existing. Please try again")

    # now grab the u_id associated with the provided token
    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    u_id = token_payload["u_id"]

    # not an authorised user
    if token not in server_data['token']:
        raise access_error.AccessError 

    for channel in server_data['channels']:
        for message in channel._messages:
            # the message is not existed
            # double check
            if message_id not in message._message_id:
                raise access_error.AccessError 
            else:
                if u_id in channels_list.channels_list(token):
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
