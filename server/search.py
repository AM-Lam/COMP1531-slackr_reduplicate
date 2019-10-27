import jwt
from .access_error import *
from .database import *

#   search(token, query_str);
#   return {messages}
#   Exception: N/A
#   Description: Given a query string, return a collection of messages  that match the query

def search(token, query_str):
    # find u_id associated with token (with non-existent database)
    DATABASE = get_data()
    admin_user_id = check_valid_token(token)

    # pull messages from a list/dictionary of all messages
    message_match = []

    # TODO: write check for if user has access to channel
    for channel in DATABASE["channels"]:
        for message in channel.get_messages():
            if query_str in message:
                message_match.append(message)

    return message_match

def check_valid_token(token):
    # find the user ID associated with this token, else raise a ValueError
    DATABASE = get_data()
    SECRET = get_secret()
    token = jwt.decode(token, SECRET, algorithms=['HS256'])

    for x in DATABASE["users"]:
        user_id = x.get_u_id()
        if user_id == token["u_id"]:
            return user_id
    raise ValueError(description="token invalid")
