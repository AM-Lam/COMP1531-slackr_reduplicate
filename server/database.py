import pickle


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


clear_data()
print("Setup complete")
