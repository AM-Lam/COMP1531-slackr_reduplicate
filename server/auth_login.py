import re
import hashlib
import jwt
import time
from flask import Flask, request
from json import dumps
from .database import *
from .access_error import *

    
def auth_login(email, password):
    update_data = get_data()

    # checking if the email has a valid structure.
    check_emailtype(email)

    # checking if the email actually exists.
    validate_email(email)
    
    # retriving the u_id if the password is correct.
    u_id = validate_password(email, password)
    
    # now we encode a unique token with the help of u_id and the current time.
    token = jwt.encode({'u_id': u_id , 'time': time.time()}, SECRET, algorithm='HS256').decode()
    
    # adding the token to the list of tokens to be killed later
    update_data["tokens"][token] = True
    
    return {"u_id": u_id, "token": token}  
     
        
def check_emailtype(email):
    # checking if the email has a valid infrastructure.
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        raise ValueError(description="this is not a valid email format!")

        
def validate_email(email):
    # checking if thr email even exists already.
    update_data = get_data()
    for clients in update_data['users']:
        if clients._email == email:
            return True
    raise ValueError(description="email does not exist on the server")


def validate_password(email, password):
    # This will check if the password to the corresponding email is correct and
    # returns user id if correct.
    update_data = get_data()
    hash_pass = (hashlib.sha256(password.encode()).hexdigest())
    for user in update_data['users']:
        if user._email == email and user._password == hash_pass:
            return user._u_id
    raise ValueError(description="wrong password please try again")
