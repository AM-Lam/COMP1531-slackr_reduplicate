import pickle
import re
import hashlib
import jwt
from datetime import datetime
from .access_error import AccessError, Value_Error


DATABASE = None
SECRET = "AVENGERS_SOCKS"


class User:
    def __init__(self, u_id, first_name, last_name, password, email, global_admin=False):
        self._u_id = u_id
        self._first_name = first_name
        self._last_name = last_name
        self._password = password
        self._email = email
        self._handle = first_name + last_name
        self._global_admin = global_admin
        self._slackr_owner = False


    def get_user_data(self):
        return {
            "u_id" : self._u_id,
            "first_name" : self._first_name,
            "last_name" : self._last_name,
            "password" : self._password,
            "email" : self._email,
            "handle" : self._handle,
        }

    def update_id(self, new_id):
        self._u_id = new_id

    def update_first_name(self, new_fname):
        self._first_name = new_fname

    def update_last_name(self, new_lname):
        self._last_name = new_lname

    def update_password(self, new_password):
        self._password = new_password

    def update_email(self, new_email):
        self._email = new_email

    def update_handle(self, new_handle):
        self._handle = new_handle

    def set_global_admin(self, admin):
        self._global_admin = admin

    def get_u_id(self):
        return self._u_id

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_password(self):
        return self._password

    def get_email(self):
        return self._email

    def get_handle(self):
        return self._handle

    def is_global_admin(self):
        return self._global_admin

    def is_slackr_owner(self):
        return self._slackr_owner


class Channel:
    def __init__(self, channel_id, channel_name, messages, creator, public):
        self._channel_id = channel_id       # id of the channel, increases
                                            # sequentially

        self._channel_name = channel_name   # channel name, string

        self._messages = messages           # messages in the channel, list
                                            # of Message objects

        self._members = creator             # members of the channel, just a list
                                            # of u_ids

        self._pinned_messages = []

        self._owners = creator.copy()       # owners of the channel, initially set to
                                            # the creator of the channel, this must
                                            # be a copy so that changing it doesn't
                                            # change members and vice-versa

        self._public = public               # is the channel public, boolean
                                            # val

        self._standup = None                # when standup is active, gives time when
                                            # standup finishes
                                            # else it's None

        self._message_id_max = 1            # a value we need to use to keep
                                            # track of the current messages id
                                            # since message_sendlater is concurrent
                                            # we need to keep track of this explicitly


    def get_channel_data(self):
        return {
            "channel_id" : self._channel_id,
            "channel_name" : self._channel_name,
            "messages" : self._messages,
            "owners" : self._owners,
            "members" : self._members,
            "owners" : self._owners,
            "public" : self._public,
            "standup" : self._standup,
        }


    def frontend_format(self):
        return {
            "channel_id" : self._channel_id,
            "name" : self._channel_name
        }

    def get_id(self):
        return self._channel_id

    def get_name(self):
        return self._channel_name

    def get_messages(self):
        return self._messages

    def get_members(self):
        return self._members

    def get_owners(self):
        return self._owners

    def is_public(self):
        return self._public

    def get_m_id(self):
        return self._message_id_max

    def get_pins(self):
        return self._pinned_messages

    def set_id(self, new_id):
        self._channel_id = new_id

    def set_name(self, name):
        self._channel_name = name

    def add_message(self, message):
        self._messages.append(message)

    def add_member(self, member):
        self._members.append(member)

    def add_owner(self, owner):
        self._owners.append(owner)

    def set_public(self, public):
        self._public = public

    def increment_m_id(self):
        self._message_id_max += 1

    def set_standup(self, standup):
        self._standup = standup

    def add_pin(self, message_id):
        self._pinned_messages.append(message_id)


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
                                            # {u_id , react_id and is_this_user_reacted}
                                            # is_this_user_reacted:whether or not the
                                            # authorised user has been one of the reacts to
                                            # this post

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
            'message': self._text,
            'time_created': self._time_sent,
            'reacts': self._reacts,
            'is_pinned': self._pinned,
        }

    def get_m_id(self):
        return self._message_id

    def get_u_id(self):
        return self._u_id

    def get_text(self):
        return self._text

    def is_pinned(self):
        return self._pinned
    
    def get_time_sent(self):
        return self._time_sent
    
    def get_reacts(self):
        return self._reacts

    def edit_text(self, new):
        self._text = new


def get_data():
    global DATABASE
    return DATABASE


def get_secret():
    global SECRET
    return SECRET


def save_data():
    global DATABASE
    with open("db_dump.p", "wb") as dump:
        pickle.dump(DATABASE, dump)


def clear_data():
    global DATABASE
    DATABASE = {
        "users" : [],
        "channels" : [],
        "tokens" : {},
        "reset" : {}
    }


# Helper Functions
def is_email_valid(email):
    # run the re module to identify if an email is valid
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    raise Value_Error(description="Email is invalid.")


def check_email_database(email):
    # check if the email is already being used/is within the database
    all_users = get_data()["users"]

    for user in all_users:
        if user.get_email() == email:
            raise Value_Error(description="Email is already in use.")

    return True


def check_valid_token(token):
    # find the user ID associated with this token, else raise a Value_Error
    db = get_data()

    if not db["tokens"].get(token, False):
        raise Value_Error(description="Invalid token")

    token_payload = jwt.decode(token, get_secret(), algorithms=['HS256'])
    u_id = token_payload["u_id"]

    for user in db["users"]:
        if u_id == user.get_u_id():
            return u_id
    raise Value_Error(description="User does not exist")


def is_handle_in_use(handle_str):
    # check if the handle is already being used/exists within the database
    users = get_data()["users"]
    
    for user in users:
        if user.get_handle() == handle_str:
            return True
    
    return False


def get_channel(channel_id):
    """
    Take a channel_id and return the channel if it exists, otherwise
    raise a Value_Error
    """
    channels = get_data()["channels"]
    for channel in channels:
        if channel.get_id() == channel_id:
            return channel
    
    raise Value_Error(description="Channel does not exist")


def get_user(u_id):
    """
    Take a u_id and return the user if it exists, otherwise
    raise a Value_Error
    """
    users = get_data()["users"]

    for user in users:
        if user.get_u_id() == u_id:
            return user
    
    raise Value_Error(description="User does not exist")


def is_user_member(u_id, channel_id):
    """
    Take a channel and a u_id, return True if the user is a member and false if
    they are not
    """

    if u_id in get_channel(channel_id).get_members():
        return True
    
    return False


def is_user_owner(u_id, channel_id):
    """
    Take a channel and a u_id, return True if the user is an owner and false if
    they are not
    """

    if u_id in get_channel(channel_id).get_owners():
        return True
    
    return False


def message_count(channel):
    """
    Take a channel and return how many messages have been sent in it
    """

    return len(channel.get_messages())


def get_message_list(channel, start, end):
    """
    Taking a Channel, a start and an end return a list of the messages
    in that channel in the order they appeared
    """
    # initialising a messages list.
    return_messages = []

    # get the messages from the channel and reverse the list to get
    # them in chronological order
    messages = channel.get_messages()[::-1]
    for message in messages[start:end]:
        return_messages.append({
            "message_id" : message.get_m_id(),
            "u_id" : message.get_u_id(),
            "message" : message.get_text(),
            "time_created" : message.get_time_sent().timestamp(),
            "reacts" : [], # message.get_reacts(),
            "is_pinned" : message.is_pinned()
        })
    
    return return_messages


def is_valid_u_id(u_id):
    """
    Take a u_id and return True if it is valid, otherwise return False
    """

    for user in get_data()["users"]:
        if user.get_u_id() == u_id:
            return True
    
    return False


def u_id_from_email(email, password):
    """
    Take an email and a password, if the user with this email also has this
    password return the u_id of the user otherwise raise an error
    """

    wrong_pasword = False
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    for user in get_data()['users']:
        if user.get_email() == email:
            if user.get_password() == hash_pass:
                return user._u_id
            wrong_pasword = True
            break
    
    if wrong_pasword:
        raise Value_Error(description="Wrong password, please try again")
    
    raise Value_Error(description="Email does not exist")


def u_id_from_email_reset(email):
    """
    Take an email to send a reset code to, if the email exists return the u_id
    otherwise raise a Value_Error
    """

    for user in get_data()['users']:
        if user.get_email() == email:
            return user._u_id
    
    raise Value_Error(description="There are no users with this password")


def check_reset_code(reset_code):
    # this will check if the reset code sent by the 
    # auth_passwordreset_request function is correct
   
    reset_codes = get_data()["reset"]
    if reset_code in reset_codes:
        email = reset_codes[reset_code]
        return email
    else:
        raise Value_Error("Reset code incorrect!")


clear_data()
print("Setup complete")