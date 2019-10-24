import jwt

#   search(token, query_str);
#   return {messages}
#   Exception: N/A
#   Description: Given a query string, return a collection of messages  that match the query

def search(token, query_str):
    # find u_id associated with token (with non-existent database)
    global DATABASE
    admin_user_id = check_valid_token(token)

    # normally we would pull messages from a list/dictionary of all messages but since that isn't implemented, we just return nothing
    messages = []
    for channels in DATABASE["channels"]:
        for message in channels["messages"]:
            # if matching
                messages.append(message);

    return messages

def check_valid_token(token):
    global DATABASE
    # find the user ID associated with this token, else raise a ValueError
    decoded_jwt = jwt.decode(token, 'sempai', algorithms=['HS256'])
    try:
        for x in DATABASE:
            if x.get("u_id") == decoded_jwt.key():
                return x.get("u_id")
    except Exception as e:
        raise ValueError("token invalid")
