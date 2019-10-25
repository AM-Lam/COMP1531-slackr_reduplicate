import pickle


DATABASE = None
SECRET = "AVENGERS_SOCKS"


class User:
    def __init__(self, u_id, first_name, last_name, password, email):
        self._u_id = u_id 
        self._first_name = first_name
        self._last_name = last_name
        self._password = password
        self._email = email
        self._handle = first_name + last_name
    
    
    def get_user_data(self):
        return {
            "u_id" : self._u_id,
            "first_name" : self._first_name,
            "last_name" : self._last_name,
            "password" : self._password,
            "email" : self._email,
            "handle" : self._handle,
        }
    

    def update_user_id(self, new_id):
        self._u_id = new_id


    def update_user_first_name(self, new_fname):
        self._first_name = new_fname


    def update_user_last_name(self, new_lname):
        self._last_name = new_lname


    def update_user_password(self, new_password):
        self._password = new_password


    def update_user_email(self, new_email):
        self._email = new_email

        
    def update_user_handle(self, new_handle):
        self._handle = new_handle


class Channel:
    def __init__(self, channel_id, channel_name, messages, members, public):
        self._channel_id = channel_id       # id of the channel, increases 
                                            # sequentially
        
        self._channel_name = channel_name   # channel name, string
        
        self._messages = messages           # messages in the channel, list
                                            # of Message objects
        
        self._members = members             # members of the channel, dictionary
                                            # with u_id as key and perm. as value
        
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
        

    def frontend_format(self):
        return {
            "channel_id" : self._channel_id,
            "name" : self._channel_name
        }

 
class Messages:
    def __init__(self, message_id, u_id, text, channel_id, time_sent, reacts):
        self._message_id = message_id       # id of the message in a channel, increases 
                                            # sequentially
        self._u_id = u_id                   # poster's u_id
        self._channel_id = channel_id       # id of the channel where the message is posted
        self._text = text                   # the content of the messages
        self._time_sent = time_sent         # time that the message is posted 
                                            # used for sendlater or standup
        self._reacts = reacts               # List of dictionaries
                                            # with u_id, react_id and is_this_user_reacted in each dictionary
                                            # is_this_user_reacted:whether or not the authorised user has been one of the reacts to this post
        self._pinned = False                # bool of whether the message is pinned or not
    

    def get_message_data(self):
        return {
            "message_id" : self._message_id,
            "u_id" : self._u_id,
            "channel_id" : self._channel_id,
            "text" : self._text,
            "time_sent" : self._time_sent,
            'reacts': self._reacts,
            'is_pinned': self._pinned,
        }

    def frontend_format(self):
        return {
            'message_id': self._message_id,
            'u_id': self._u_id,
            'message': self._test,
            'time_created': self._time_sent,
            'reacts': self._reacts,
            'is_pinned': self._pinned,
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
    "tokens" : {},
    "reset" : {} # <----- I am adding this field {'reset_code':'email'} <-to be able to store the reset
                                     # code and to delete the code after the new password has been made
})

print("Setup complete")
