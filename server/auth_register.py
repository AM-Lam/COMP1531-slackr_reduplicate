import re
import hashlib
import jwt
from flask import Flask, request
from json import dumps
from database import *
app = Flask(__name__)


def auth_register(email, password, name_first, name_last):
    @app.route("/user/register", methods=['POST'])
    def register():
        SECRET = 'avengers_suck'
        u_id = request.form.get('u_id')
        token = jwt.encode({'u_id':u_id}, SECRET, algorithm='HS256')
        first_name = request.form.get('first_name')
        check_first(first_name)
        last_name = request.form.get('last_name')
        check_last(last_name)
        password = request.form.get('password')
        hashed = check_password_strength(password)
        email = request.form.get('email')
        check_regEmailtype(email)
        validate_regEmail(email)

        person = User(u_id,first_name,last_name,hashed,email,token)
        update_data['users'].append(person)
        
        return {"u_id": u_id, "token": token}

def check_regEmailtype(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        raise ValueError("this is not a valid email format!")

def validate_regEmail(email):
    flag = 0
    for clients in update_data['users']:
        if clients.email == email:
            flag = 1
    if flag == 1:
        raise ValueError("email already exists on the server")

def check_password_strength(password):
    # to check if the password is at least 5 digits
    if len(password) >= 6:
        return (hashlib.sha256(password.encode()).hexdigest())
    else:
        raise ValueError("Password is too short!")

def check_first(first_name):
    # not more than 50 characters 
    if len(first_name) < 50:
        return True
    else:
        raise ValueError("first name is too long!")

def check_last(last_name):
    # not more than 50 characters
    if len(last_name) < 50:
        return True
    else:
        raise ValueError("last name is too long!")


if __name__ == '__main__':
    app.run(debug = True , port = 3006)