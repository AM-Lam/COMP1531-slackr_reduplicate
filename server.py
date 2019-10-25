"""Flask server"""
import sys
import atexit
from flask_cors import CORS
from json import dumps
from flask import Flask, request
from flask_mail import Mail, Message
from server import *


APP = Flask(__name__)
CORS(APP)

APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'deadthundersquirrels@gmail.com',
    MAIL_PASSWORD = "passnew%1"
)



@APP.route('/auth/register', methods=['POST'])
def register():
    first_name = request.form.get('name_first')
    last_name = request.form.get('name_last')
    password = request.form.get('password')
    email = request.form.get('email')
    dumpstring = auth_register.auth_register(email, password, first_name, last_name)
    return dumps (dumpstring)

@APP.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    dumpstring = auth_login.auth_login(email, password)
    return dumps (dumpstring)

@APP.route('/auth/logout', methods=['POST'])
def user_logout():
    token = request.form.get('token')
    dumpstring = auth_logout.auth_logout(token)
    return dumps (dumpstring)

@APP.route('/auth/passwordreset/request', methods=['POST'])
def email_request():
    email = request.form.get('email')
    dumpstring = auth_passwordreset_request.auth_passwordreset_request(email)
    return dumps (dumpstring)

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def email_reset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    dumpstring = auth_passwordreset_reset.auth_passwordreset_reset(reset_code, new_password)
    return dumps (dumpstring)
    
@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })


@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })


@APP.route('/channels/create', methods=["POST"])
def run_channels_create():
    """ 
        run the channels_create function to make a new channel and
        add it to the  server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = channels_create.channels_create(
            request_data["token"],
            request_data["name"],
            bool(request_data["is_public"])
        )
    except:
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

    # when the server exists dump the current database into a file
    atexit.register(database.save_data)
