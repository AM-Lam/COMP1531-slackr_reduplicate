import hashlib
import random
import string
from .database import *
from flask_mail import Mail, Message


def auth_passwordreset_request(email):
    userid = validate_email_existence(email)    # this checks if the givin email even exists and retrives id.
    send_code(email, userid)                    # this function sends the code through the SMTP setup.
    return {}

def validate_email_existence(email):
    # flag is zero if email does not exist and one if it does.
    flag = 0
    userid = None
    for clients in update_data['users']:
        if clients._email == email:
            flag = 1
            userid = clients._u_id
    if flag == 0:
        raise ValueError("email does not exist")
    else:
        return userid

def send_code(email, user_id):
    mail = Mail(APP)
    try:
        msg = Message("Your slacky reset code",
            sender="deadthundersquirrels@gmail.com",
            recipients=[email])
        random_num = user_id * (random.randint(1,10000))      # multiplying a random number to user id.
        random_alph = random.choice(string.ascii_letters)     # getting a random alphabet
        ramdom_str = str(random_num) + random_alph            # appending the two toghter
        code = (hashlib.sha256(random_str.encode()).hexdigest())  # hashing the code
        update_data["reset"][code] = email #<-------- Is this correct?
        msg.body = "your reset code is " + code
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return (str(e))

