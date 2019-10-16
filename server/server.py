from modules import *
from flask import Flask
from json import dumps


APP = Flask(__name__)


@APP.route("/")
def index():
    return "Test\n"


if __name__ == "__main__":
    APP.run()