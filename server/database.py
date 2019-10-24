import pickle


DATABASE = None
SECRET = "MICHELFOUCAULT"


class User:
    def __init__(self, u_id, first_name, last_name, password, email, token):
        self._u_id = u_id 
        self._first_name = first_name
        self._last_name = last_name
        self._password = password
        self._email = email
        self._handle = first_name + last_name
        self._token = token
    
    
    def get_user_data(self):
        return {
            "u_id" : self._u_id,
            "first_name" : self._first_name,
            "last_name" : self._last_name,
            "password" : self._password,
            "email" : self._email,
            "handle" : self._handle,
            "token" : self._token,
        }
    

    def update_user_data(self, new_data):
        self._u_id = new_data["u_id"]
        self._first_name = new_data["first_name"]
        self._last_name = new_data["last_name"]
        self._password = new_data["password"]
        self._email = new_data["email"]
        self._handle = new_data["handle"]
        self._token = new_data["token"]


class Channel:
    def __init__(self, channel_id, channel_name, messages, members, public):
        self._channel_id = channel_id       # id of the channel, increases 
                                            # sequentially
        
        self._channel_name = channel_name   # channel name, string
        
        self._messages = messages           # messages in the channel, list
                                            # of Message objects
        
        self._members = members             # members of the channel, list of
                                            # u_ids
        
        self._public = public               # is the channel public, boolean 
                                            # val
    

    def get_channel_data(self):
        return {
            "channel_id" : self._channel_id,
            "channel_name" : self._channel_name,
            "messages" : self._messages,
            "members" : self._members,
            "public" : self._public,
        }
    

    def update_channel_data(self, new_data):
        self._channel_id = new_data["channel_id"]
        self._first_name = new_data["first_name"]
        self._last_name = new_data["last_name"]
        self._password = new_data["password"]
        self._email = new_data["email"]
        
    def add_message(self, message_id, u_id, text, channel_id, time_sent):
        message = Messages(message_id, u_id, text, channel_id, time_sent)
        self._messages.append(message)

class Messages:
    def __init__(self, message_id, u_id, text, channel_id, time_sent):
        self._message_id = message_id
        self._u_id = u_id
        self._channel_id = channel_id
        self._text = text
        self._time_sent = time_sent
    

    def get_message_data(self):
        return {
            "message_id" : self._message_id,
            "u_id" : self._u_id,
            "channel_id" : self._channel_id,
            "text" : self._text,
            "time_sent" : self._time_sent,
        }


def get_data():
    global DATABASE
    return DATABASE


def update_data(new_database):
    global DATABASE
    DATABASE = new_database
    return DATABASE


def get_secret():
    global SECRET
    return SECRET


def save_data():
    global DATABASE
    with open("db_dump.p", "wb") as dump:
        pickle.dump(DATABASE, dump)


# initialise an empty database
update_data({
    "users" : [],
    "channels" : [],
    "tokens" : {}
})

print("Setup complete")
