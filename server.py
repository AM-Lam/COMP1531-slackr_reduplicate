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


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

    # when the server exists dump the current database into a file
    atexit.register(database.save_data)
