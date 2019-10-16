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
        self.__u_id = u_id 
        self.__first_name = firstName
        self.__last_name = lastName
        self.__password = password
        self.__email = email
        self.__handle = firstName + lastName


class channel:
    def __init__(self, channel_id, channel_name, message_id, member, public):
        self.__channel_id = channel_id
        self.__channel_name = channel_name
        self.__message_id = message_id
        self.__member = member     
        self.__public = True #default

class messages:
    def __init__(self, message_id, u_id, text, channel_id, time_stamps):
        self.__message_id = message_id
        self.__u_id = u_id
        self.__text = text
        self.__channel_id = channel_id
        self.__time_stamps = time_stamps