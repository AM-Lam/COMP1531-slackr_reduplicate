import re
import time
import hashlib
import jwt
from flask import Flask, request
from json import dumps
from .database import * 
from .access_error import *


def auth_register(email, password, first_name, last_name):
    update_data = get_data()
    
    check_first(first_name)
    check_last(last_name)
    
    # checking if password is strong and getting a hash.
    hashed = check_password_strength(password)
    
    # checking if the email has a valid structure.
    check_regEmailtype(email)
    
    # checking if the email already exists.
    validate_regEmail(email)

    # getting the number of currently registered users.
    listlen = len(update_data['users'])
    
    # new user id is the number of current users plus one.
    u_id = listlen + 1
    
    # now we encode a unique token with the help of u_id and the current time.
    token = jwt.encode({'u_id': u_id , 'time': time.time()}, get_secret(), algorithm='HS256').decode()
    
    # adding the token to the list of tokens to be killed later.
    update_data["tokens"][token] = True   
    
    # creating a user class instance.
    person = User(u_id,first_name,last_name,hashed,email)

    # if this is the first user to register make them a slackr owner
    if u_id == 1:
        person.set_global_admin(True)
        person._slackr_owner = True
    
    # adding the person to the user list.
    update_data['users'].append(person)
    
    return {"u_id": u_id, "token": token}


def check_regEmailtype(email):
    # checking if the email has a valid infrastructure.
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        raise ValueError(description="this is not a valid email format!")


def validate_regEmail(email):
    # checking if thr email even exists already.
    flag = 0
    update_data = get_data()
    for clients in update_data['users']:
        if clients._email == email:
            flag = 1
    if flag == 1:
        raise ValueError("email already exists on the server")
    else:
        return True


def check_password_strength(password):
    # to check if the password is at least 6 digits.
    if len(password) >= 6:
        return (hashlib.sha256(password.encode()).hexdigest())
    else:
        raise ValueError("Password is too short! Atleast put in a bit of effort!")


def check_first(first_name):
    # first name should not be more than 50 characters.
    if len(first_name) < 50:
        return True
    else:
        raise ValueError("first name is too long!")


def check_last(last_name):
    # last name should not be more than 50 characters.
    if len(last_name) < 50:
        return True
    else:
        raise ValueError("last name is too long!")