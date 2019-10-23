import re
import hashlib
import jwt
from flask import Flask, request
from json import dumps
from database import *
app = Flask(__name__)
    
@app.route("/user/login", methods=['POST'])
def auth_login(email, password):
    SECRET = 'avengers_suck'
    
    email = request.form.get('email')
    check_emailtype(email)
    validate_email(email)
    password = request.form.get('password')
    validate_password(email, password)      
    return {"u_id": uid, "token": token}  
     
        
def check_emailtype(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        raise ValueError("this is not a valid email format!")

        
def validate_email(email):
    flag = 0
    for clients in update_data['users']:
        if clients.email == email:
            flag = 1
    if flag == 1:
        raise ValueError("email already exists on the server")


def validate_password(email, password):
    # This will check if the password to the corresponding email is correct
    flag = 0
    hash_pass = (hashlib.sha256(password.encode()).hexdigest())
    for user in update_data['users']:
        if user.email == email and user.password == hash_pass:
            flag = 1
    if flag = 0:
        raise ValueError("wrong password please try again")
         
if __name__ == '__main__':
    app.run(debug = True , port = 3006)


'''
for user in update_data['users']:
    if user.email == 
'''