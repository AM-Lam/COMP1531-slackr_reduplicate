# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=R0902
# pylint: disable=R0913
# pylint: disable=R0904

import pickle
import re
import hashlib
import jwt
from .access_error import Value_Error


DATABASE = None
SECRET = "AVENGERS_SOCKS"


class User:
    def __init__(self, u_id, first_name, last_name, password, email,
                 global_admin=False):
        self._u_id = u_id
        self._first_name = first_name
        self._last_name = last_name
        self._password = password
        self._email = email
        self._handle = first_name + last_name
        self._global_admin = global_admin
        self._slackr_owner = False
        self._profile_img_url = "static/profile_images/default.jpg"

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

    def set_profile_img_url(self, img_url):
        self._profile_img_url = img_url

    def set_slackr_owner(self, owner):
        self._slackr_owner = owner

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

    def get_profile_img_url(self):
        return self._profile_img_url


class Channel:
    def __init__(self, channel_id, channel_name, messages, creator, public):
        self._channel_id = channel_id
        self._channel_name = channel_name

        # messages, list of Messages objects
        self._messages = messages

        # members of the channel, list of uids
        self._members = creator

        self._pinned_messages = []

        # owners of the channel, initially just the creator, this is
        # a copy so that changing it doesn't affect the members and
        # vice-versa
        self._owners = creator.copy()

        # is the channel public? boolean value
        self._public = public

        # a dictionary representing the status of a standup, has the
        # structure:
        # {time_finish : time,
        #  is_active : bool,
        #  messages : str,
        #  start_user : User}
        self._standup = {"time_finish": None, "is_active": False,
                         "messages": "", "start_user": None}

        # keeps track of the next message_id to be given out, stored
        # like this so that message_sendlater and message_send don't
        # get clashing ids
        self._message_id_max = 1

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
        return list(set(self._owners + list(
            filter(lambda x: is_user_member(x, self.get_id()), get_admins())
        )))

    def is_public(self):
        return self._public

    def get_m_id(self):
        return self._message_id_max

    def get_standup(self):
        return self._standup

    def get_pins(self):
        return self._pinned_messages

    def get_message(self, m_id):
        for message in self.get_messages():
            if message.get_m_id() == m_id:
                return message

        raise Value_Error(description="Message does not exist")

    def set_name(self, name):
        self._channel_name = name

    def add_message(self, message):
        self._messages.append(message)

    def remove_message(self, message):
        self._messages.remove(message)

    def add_member(self, member):
        self._members.append(member)

    def remove_member(self, member):
        self._members.remove(member)

    def add_owner(self, owner):
        self._owners.append(owner)

    def remove_owner(self, owner):
        self._owners.remove(owner)

    def set_public(self, public):
        self._public = public

    def increment_m_id(self):
        self._message_id_max += 1

    def set_standup(self, standup):
        self._standup = standup

    def add_pin(self, message_id):
        self._pinned_messages.append(message_id)

    def remove_pin(self, message_id):
        self._pinned_messages.remove(message_id)


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

    def frontend_format(self, u_id):
        return {
            "message_id": self.get_m_id(),
            "u_id": self.get_u_id(),
            "message": self.get_text(),
            "time_created": self.get_time_sent().timestamp(),
            "reacts": self.get_reacts_frontend(u_id),
            "is_pinned": self.is_pinned()
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

    def get_reacts_frontend(self, u_id):
        # build react list with the right format
        react_list = []
        for react in self.get_reacts():
            react_list.append({
                "react_id" : react["react_id"],
                "u_ids" : react["u_ids"],
                "is_this_user_reacted" : u_id in react["u_ids"]
            })
        return react_list

    def set_pinned(self, pinned):
        self._pinned = pinned

    def edit_text(self, new):
        self._text = new


def get_data():
    return DATABASE


def get_secret():
    return SECRET


def save_data():
    with open("db_dump.p", "wb") as dump:
        pickle.dump(DATABASE, dump)


def clear_data():
    # pylint: disable=W0603
    global DATABASE
    DATABASE = {
        "users" : {},
        "channels" : {},
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

    for u_id in all_users:
        user = all_users[u_id]
        if user.get_email() == email:
            raise Value_Error(description="Email is already in use.")

    return True


def check_valid_token(token):
    """
    Find the user ID associated with this token, else raise a
    Value_Error
    """

    server_data = get_data()

    # Is this token currently active? If not raise an error
    if not server_data["tokens"].get(token, False):
        raise Value_Error(description="Invalid token")

    token_payload = jwt.decode(token, get_secret(), algorithms=['HS256'])
    u_id = token_payload["u_id"]

    # if the u_id exists return it, otherwise raise an error
    if u_id in server_data["users"]:
        return u_id

    raise Value_Error(description="User does not exist")


def is_handle_in_use(handle_str):
    # check if the handle is already being used/exists within the database
    users = get_data()["users"]

    for u_id in users:
        user = users[u_id]
        if user.get_handle() == handle_str:
            return True

    return False


def get_channel(channel_id):
    """
    Take a channel_id and return the channel if it exists, otherwise
    raise a Value_Error
    """
    channels = get_data()["channels"]

    try:
        return channels[channel_id]
    except KeyError:
        raise Value_Error(description="Channel does not exist")


def get_user(u_id):
    """
    Take a u_id and return the user if it exists, otherwise
    raise a Value_Error
    """
    users = get_data()["users"]

    try:
        return users[u_id]
    except KeyError:
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


def get_message_list(channel, start, end, u_id):
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
        return_messages.append(message.frontend_format(u_id))

    return return_messages


def is_valid_u_id(u_id):
    """
    Take a u_id and return True if it is valid, otherwise return False
    """

    return u_id in get_data()["users"]


def u_id_from_email(email, password):
    """
    Take an email and a password, if the user with this email also has this
    password return the u_id of the user otherwise raise an error
    """
    users = get_data()["users"]

    wrong_pasword = False
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()

    for u_id in users:
        user = users[u_id]

        if user.get_email() == email:
            if user.get_password() == hashed_pass:
                return u_id

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
    users = get_data()["users"]

    for u_id in users:
        user = users[u_id]

        if user.get_email() == email:
            return u_id

    raise Value_Error(description="There are no users with this email")


def check_reset_code(reset_code):
    # this will check if the reset code sent by the
    # auth_passwordreset_request function is correct

    reset_codes = get_data()["reset"]
    if reset_code in reset_codes:
        email = reset_codes[reset_code]
        return email

    raise Value_Error("Reset code incorrect!")


def get_admins():
    # get all the admins/slackr owners, they have
    # permissions in all channels so we should add
    # them to the owners list
    admins = []
    users = get_data()["users"]

    for u_id in get_data()["users"]:
        user = users[u_id]
        if user.is_global_admin() or user.is_slackr_owner():
            admins.append(u_id)

    return admins


clear_data()
print("Setup complete")
