"""Flask server"""
import sys
import atexit
from flask_cors import CORS
from json import dumps
from flask import Flask, request
from server import *


APP = Flask(__name__)
CORS(APP)


@APP.route('/auth/register', methods=['POST'])
def echo4():
    pass


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

@APP.route('/message/send', methods=["POST"])
def run_message_send():
    """ 
        run the message_send function to send a message and
        add it to the  server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = message_send.message_send(
            request_data["token"],
            request_data["channel_id"],
            request_data["message"]
        )
    except: # add more error
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)

@APP.route('/message/remove', methods=["DELETE"])
def run_message_remove():
    """ 
        run the message_remove function to remove a message and
        update the server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = message_remove.message_remove(
            request_data["token"],
            request_data["message_id"]
        )
    except: # add more error
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)

@APP.route('/message/edit', methods=["PUT"])
def run_message_edit():
    """ 
        run the message_edit function to edit a message and
        update the server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = message_edit.message_edit(
            request_data["token"],
            request_data["message_id"],
            request_data["message"]
        )
    except: # add more error
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)

@APP.route('/message/react', methods=["POST"])
def run_message_react():
    """ 
        run the message_react function to react a message and
        add it to the server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = message_react.message_react(
            request_data["token"],
            request_data["message_id"],
            request_data["react_id"]
        )
    except: 
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)

@APP.route('/message/unreact', methods=["POST"])
def run_message_unreact():
    """ 
        run the message_react function to react a message and
        add it to the server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = message_unreact.message_unreact(
            request_data["token"],
            request_data["message_id"],
            request_data["react_id"]
        )
    except: # add more error
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)


@APP.route('/message/pin', methods=["POST"])
def run_message_pin():
    """ 
        run the message_react function to react a message and
        add it to the server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = message_pin.message_pin(
            request_data["token"],
            request_data["message_id"]
        )
    except: # add more error
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)

@APP.route('/message/unpin', methods=["POST"])
def run_message_unpin():
    """ 
        run the message_react function to react a message and
        add it to the server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = message_unpin.message_unpin(
            request_data["token"],
            request_data["message_id"]
        )
    except: # add more error
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)

@APP.route('/user/profile', methods=["GET"])
def run_user_profile():
    """ 
        run the message_react function to react a message and
        add it to the server database
    """
    request_data = request.get_json()
    return_value = ""
    try:
        return_value = user_profile.user_profile(
            request_data["token"],
            request_data["u_id"]
        )
    except: # add more error
        return_value = "<h1>403 Request Forbidden</h1>"
    
    return dumps(return_value)

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

    # when the server exists dump the current database into a file
    atexit.register(database.save_data)
