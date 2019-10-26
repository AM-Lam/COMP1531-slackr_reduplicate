"""Flask server"""
import sys
import atexit
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_mail import Mail, Message
from server import *


def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)
mail = Mail(APP)
class ValueError(HTTPException):
    code = 400
    message = 'No message specified'


APP.config.update({
    'MAIL_SERVER' : 'smtp.gmail.com',
    'MAIL_PORT': '465',
    'MAIL_USE_SSL' : True,
    'MAIL_USE_TLS' : False,
    'MAIL_USERNAME' : 'deadthundersquirrels@gmail.com',
    'MAIL_PASSWORD' : "passnew%1"
})
print(APP.config['TESTING'])


@APP.route('/auth/register', methods=['POST'])
def register():
    first_name = request.form.get('name_first')
    last_name = request.form.get('name_last')
    password = request.form.get('password')
    email = request.form.get('email')
    try:
        dumpstring = auth_register.auth_register(email, password, first_name, last_name)
    except ValueError as error:
        defaultHandler(error)
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
    print(send_code(email, dumpstring))
    return dumps({})

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def email_reset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    dumpstring = auth_passwordreset_reset.auth_passwordreset_reset(reset_code, new_password)
    return dumps (dumpstring)

@APP.route('/channel/invite', methods=['POST'])
def channel_invite_e():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    dumpstring = channel_invite.channel_invite(token,channel_id,u_id)
    return (dumpstring)

@APP.route('/channel/details', methods=['GET'])
def channel_details_e():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    dumpstring = channel_details.channel_details(token,channel_id)
    return (dumpstring)

@APP.route('/channel/messages', methods=['GET'])
def channel_messages_e():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    start = request.form.get('start')
    dumpstring = channel_messages.channel_messages(token,channel_id, start)
    return (dumpstring)
    
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


@APP.route("/channel/leave", methods=["POST"])
def run_channel_leave():
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = channel_leave.channel_leave(
            request_data["token"],
            request_data["channel_id"]
        )
    except:
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)


@APP.route('/channels/listall', methods=["POST"])
def run_channels_listall():
    """
    Retrieve a list of all the channels that have been created and return
    as a list of dictionaries. At the moment we are assuming that all users
    can do this, regardless of what their token is but I will follow this up
    with the stakeholders.
    """
    request_data = request.get_json()
    return_value = ""

    try:
        return_value = channels_listall.channels_listall(
            request_data["token"]
        )
    except Exception as e:
        if e == access_error.AccessError:
            return_value = "<h1>403 Access Forbidden</h1>"
        else:
            return_value = "<h1>404 Page Not Found</h1>"
    
    return dumps(return_value)

def send_code(email, user_id):
    try:
        with APP.app_context():
            msg = Message(subject = "Your slacky reset code",
                sender="deadthundersquirrels@gmail.com",
                recipients=[email],
                body = 'hello')
            random_num = user_id * (random.randint(1,10000))      # multiplying a random number to user id.
            random_alph = random.choice(string.ascii_letters)     # getting a random alphabet
            ramdom_str = str(random_num) + random_alph            # appending the two toghter
            code = (hashlib.sha256(random_str.encode()).hexdigest())  # hashing the code
            update_data["reset"][code] = email # adding the code email combo to the database for future refrence.
            msg.body = "your reset code is " + code
           
            mail.send(msg)
            return {}
    except Exception as e:
        return (str(e))




if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

    # when the server exists dump the current database into a file
    atexit.register(database.save_data)

