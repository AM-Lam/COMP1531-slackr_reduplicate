"""Flask server"""
import sys
import atexit
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_mail import Mail, Message
from datetime import datetime
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
    print(send_code(email, dumpstring)) # remove later
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
    return_value = channels_create.channels_create(request_data["token"],
                                                   request_data["name"],
                                                   bool(request_data["is_public"]))
    
    return dumps(return_value)


@APP.route("/channel/leave", methods=["POST"])
def run_channel_leave():
    request_data = request.get_json()
    return_value = channel_leave.channel_leave(request_data["token"],
                                               request_data["channel_id"])
    
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
    return_value = channels_listall.channels_listall(request_data["token"])
    
    return dumps(return_value)


@APP.route('/channels/list', methods=['POST'])
def run_channels_list():
    request_data = request.get_json()
    return_value = channels_list.channels_list(
        request_data["token"]
    )
    
    return dumps(return_value)


@APP.route('/channel/join', methods=['POST'])
def run_channel_join():
    request_data = request.get_json()
    return_value = return_value = channel_join.channel_join(
        request_data["token"], 
        request_data["channel_id"]
    )
    
    return dumps(return_value)

def send_code(email, code):
    try:
        with APP.app_context():
            msg = Message(subject = "Your slacky reset code",
                sender="deadthundersquirrels@gmail.com",
                recipients=[email],
                body = 'hello')
            msg.body = "your reset code is " + code
            mail.send(msg)
            return {}
    except Exception as e:
        return (str(e))




@APP.route('/channel/addowner', methods=["POST"])
def run_channel_addowner():
    request_data = request.get_json()
    return_value = channel_addowner.channel_addowner(
        request_data["token"],
        request_data["channel_id"],
        request_data["u_id"]
    )

    return dumps(return_value)



@APP.route('/channel/removeowner', methods=["POST"])
def run_channel_removeowner():
    request_data = request.get_json()
    return_value = channel_addowner.channel_addowner(
        request_data["token"],
        request_data["channel_id"],
        request_data["u_id"]
    )

    return dumps(return_value)


@APP.route('/message/sendlater')
def run_message_sendlater():
    request_data = request.get_json()
    return_value = channel_addowner.channel_addowner(
        request_data["token"],
        request_data["channel_id"],
        request_data["message"],
        datetime.utcfromtimestamp(request_data["time_sent"])
    )

    return dumps(return_value)


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

    # when the server exists dump the current database into a file
    atexit.register(database.save_data)

