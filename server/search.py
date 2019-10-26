#   search(token, query_str);
#   return {messages}
#   Exception: N/A
#   Description: Given a query string, return a collection of messages  that match the query

def search(token, query_str):
    global DATABASE
    # find u_id associated with token (with non-existent database)
    admin_user_id = check_valid_token(token)

    # pull messages from a list/dictionary of all messages
    message_match = []
    
    # TODO: write check for if user has access to channel
    for channels in DATABASE["channels"]:
        channel_dictionary = channels.get_channel_data()
        messages_list = channel_dictionary["messages"]
        for message in messages_list:
            if query_str in message:
                message_match.append(message);

    return messages

def check_valid_token(token):
    global DATABASE
    # find the user ID associated with this token, else raise a ValueError
    try:
        for x in DATABASE:
            if x.get("token") == token:
                return x.get("u_id")
    except Exception as e:
        raise ValueError("token invalid")
