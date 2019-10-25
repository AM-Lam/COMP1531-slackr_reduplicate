import re
import hashlib
import jwt
from flask import Flask, request
from json import dumps
from .database import *

    
def auth_login(email, password):
    SECRET = get_secret()       # getting the secret from the database.
    check_emailtype(email)      # checking if the email has a valid structure.
    validate_email(email)       # checking if the email actually exists.
    u_id = validate_password(email, password)   # retriving the u_id if password is correct.
    # now we encode a unique token with the help of u_id and the current time.
    token = jwt.encode({'u_id': u_id , 'time': time.time()}, SECRET, algorithm='HS256').decode()
    update_data["tokens"][token] = True   # adding the token to the list of tokens to be killed later.      
    return {"u_id": u_id, "token": token}  
     
        
def check_emailtype(email):
    # checking if the email has a valid infrastructure.
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        raise ValueError("this is not a valid email format!")

        
def validate_email(email):
    # checking if thr email even exists already.
    flag = 0
    for clients in update_data['users']:
        if clients._email == email:
            flag = 1
    if flag == 0:
        raise ValueError("email already exists on the server")


def validate_password(email, password):
    # This will check if the password to the corresponding email is correct and returns user id if correct.
    flag = 0
    hash_pass = (hashlib.sha256(password.encode()).hexdigest())
    for user in update_data['users']:
        if user._email == email and user._password == hash_pass:
            flag = 1
            return user._u_id
    if flag == 0:
        raise ValueError("wrong password please try again")
