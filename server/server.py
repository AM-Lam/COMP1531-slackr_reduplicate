from flask import Flask


APP = Flask(__name__)


@APP.route("/")
def index():
    return "Test\n"


if __name__ == "__main__":
    APP.run()