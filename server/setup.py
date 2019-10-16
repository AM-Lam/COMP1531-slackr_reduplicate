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
        self.u_id = u_id 
        self.first_name = firstName
        self.last_name = lastName
        self.password = password
        self.email = email
        self.handle = firstName + lastName


class channel:
    def __init__(self, channel_id, channel_name, message_id, member, public):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.message_id = message_id
        self.member = member     
        self.public = True #default

class messages:
    def __init__(self, message_id, u_id, text, channel_id, time_stamps):
        self.message_id = message_id
        self.u_id = u_id
        self.text = text
        self channel_id = channel_id
        self.time_stamps = time_stamps