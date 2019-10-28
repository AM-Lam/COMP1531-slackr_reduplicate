import hashlib
import random
import string
from flask_mail import Mail, Message
from .database import get_data
from .access_error import *


def auth_passwordreset_request(email):
    update_data = get_data()
    user_id = validate_email_existence(email)    # this checks if the givin email even exists and retrives id.
    # send_code(email, userid, APP)                    # this function sends the code through the SMTP setup.
    random_num = user_id * (random.randint(1,10000))      # multiplying a random number to user id.
    random_alph = random.choice(string.ascii_letters)     # getting a random alphabet
    random_str = str(random_num) + random_alph            # appending the two toghter
    code = (hashlib.sha256(random_str.encode()).hexdigest())  # hashing the code
    update_data["reset"][code] = email # adding the code email combo to the database for future refrence.
    return code

def validate_email_existence(email):
    # flag is zero if email does not exist and one if it does.
    update_data = get_data()
    flag = 0
    userid = None
    for clients in update_data['users']:
        if clients._email == email:
            flag = 1
            userid = clients._u_id
    if flag == 0:
        raise ValueError(description="email does not exist")
    else:
        return userid
