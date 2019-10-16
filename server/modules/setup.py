from modules import *

DATABASE = None


def get_data():
    global DATABASE
    return DATABASE


def update_data(new_database):
    global DATABASE
    DATABASE = new_database
    return DATABASE


# initialise an empty database
update_data({
    "users" : [],
    "channels" : []
})

print("Setup complete")

class User:
    def __init__(self, u_id, firstName, lastName, password, email):
        self._u_id = u_id 
        self._first_name = firstName
        self._last_name = lastName
        self._password = password
        self._email = email
        self._handle = firstName + lastName

    def get_data(self, key):
        return self.key

    def set_data(self, key, data):
        self.key = data


class channel:
    def __init__(self, channel_id, channel_name, message_id, member, public):
        self._channel_id = channel_id
        self._channel_name = channel_name
        self._message_id = message_id
        self._member = member     
        self._public = True #default

    def get_data(self, key):
        return self.key

    def set_data(self, key, data):
        self.key = data

    # update member list with a new list
    def update_member_list(self, list):
        self.member = list

    def change_public(self):
        if self._public == True:
            self._public = False
        else 
            self._public = True

class messages:
    def __init__(self, message_id, u_id, text, channel_id, time_stamps):
        self._message_id = message_id
        self._u_id = u_id
        self._text = text
        self._channel_id = channel_id
        self._time_stamps = time_stamps

    def get_data(self, key):
        return self.key

    def set_data(self, key, data):
        self.key = data