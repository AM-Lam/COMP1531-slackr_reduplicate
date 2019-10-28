import time
import random
import hashlib
import string
import jwt
from .database import get_data, get_secret, User
from .access_error import *


def auth_login(email, password):
    update_data = get_data()

    # checking if the email has a valid structure.
    check_emailtype(email)

    # checking if the email actually exists.
    validate_email(email)
    
    # retriving the u_id if the password is correct.
    u_id = validate_password(email, password)
    
    # now we encode a unique token with the help of u_id and the current time.
    token = jwt.encode({'u_id': u_id , 'time': time.time()}, get_secret(),
                       algorithm='HS256').decode()
    
    # adding the token to the list of tokens to be killed later
    update_data["tokens"][token] = True
    
    return {"u_id": u_id, "token": token}


def auth_logout(token):
    update_data = get_data()
    
    # if the token is active
    if token in update_data["tokens"]:
        # deleting the token from existence.
        del update_data["tokens"][token]
        
        # now that the token has been deleted we return true
        return {'is_success' : True}
    raise ValueError(description="session token is already invalid")


def auth_passwordreset_request(email):
    update_data = get_data()
    
    # this checks if the givin email even exists and retrives id.
    user_id = validate_email_existence(email)
    
    # send_code(email, userid, APP)
    
    # multiplying a random number to user id.
    random_num = user_id * (random.randint(1,10000))
    
    # getting a random alphabet
    random_alph = random.choice(string.ascii_letters)

    # appending the two toghter
    random_str = str(random_num) + random_alph

    # hashing the code
    code = (hashlib.sha256(random_str.encode()).hexdigest())

    # adding the code email combo to the database for future refrence.
    update_data["reset"][code] = email
    
    return code


def auth_passwordreset_reset(reset_code, new_password):
    update_data = get_data()

    # check if the reset code is valid and retrive the email
    email = check_reset_code(reset_code)

    # if the password is strong enough
    if chec_password_strength(new_password) == True:

        # finding the user in the list of users
        for users in update_data['users']:

            # looking for the user in the users list in the database.
            if users._email == email:
                # hashing the new password
                hashed_pass = (hashlib.sha256(new_password.encode()).hexdigest())
                # updating the old password
                users.update_user_password(hashed_pass)

                # once the password is updated, delete the reset_code
                del update_data["reset"][reset_code]
    return {}


def auth_register(email, password, first_name, last_name):
    update_data = get_data()
    
    check_first(first_name)
    check_last(last_name)
    
    # checking if password is strong and getting a hash.
    hashed = check_password_strength(password)
    
    # checking if the email has a valid structure.
    check_regEmailtype(email)
    
    # checking if the email already exists.
    validate_regEmail(email)

    # getting the number of currently registered users.
    listlen = len(update_data['users'])
    
    # new user id is the number of current users plus one.
    u_id = listlen + 1
    
    # now we encode a unique token with the help of u_id and the current time.
    token = jwt.encode({'u_id': u_id , 'time': time.time()}, get_secret(), algorithm='HS256').decode()
    
    # adding the token to the list of tokens to be killed later.
    update_data["tokens"][token] = True   
    
    # creating a user class instance.
    person = User(u_id,first_name,last_name,hashed,email)

    # if this is the first user to register make them a slackr owner
    if u_id == 1:
        person.set_global_admin(True)
        person._slackr_owner = True
    
    # adding the person to the user list.
    update_data['users'].append(person)
    
    return {"u_id": u_id, "token": token}


def admin_userpermission_change(token, u_id, p_id):
    server_data = get_data()

    if not server_data["tokens"].get(token, False):
        raise AccessError(description="Invalid token")

    token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
    request_u_id = token_payload["u_id"]

    request_user = None
    user = None
    for u in server_data["users"]:
        if u.get_u_id() == u_id:
            user = u
        if u.get_u_id() == request_u_id:
            request_user = u
        if not request_u_id and not user:
            break
    
    if user == None:
        raise ValueError(description="u_id does not refer to a real user")
    
    if request_user == None:
        raise ValueError(description="Request does not come from a real user")
    
    if not (request_user.is_global_admin() or request_user.is_slackr_owner()):
        raise AccessError(description="You do not have permissions to do this")

    if not (1 <= p_id <= 3):
        raise ValueError(description=f"{p_id} is not a valid permission id")
    
    # global admins cannot change the perms of slackr owners
    if not request_user.is_slackr_owner() and user.is_slackr_owner():
        raise AccessError(description="You do not have permissions to do this")

    # handle the perm changes
    if p_id == 1:
        # make the user a slackr owner, only other slackr owners can do this
        if not request_user.is_slackr_owner():
            raise AccessError(description="You do not have permissions to do this")
        user._slackr_owner = True
        user.set_global_admin(True)
    elif p_id == 2:
        # make the user a global admin, this should always be possible if we
        # reach this point
        user._slackr_owner = False
        user.set_global_admin(True)
    else:
        # make the user a regular member, this should also always be possible
        # if we reach this point
        user._slackr_owner = False
        user.set_global_admin(False)
    
    return {}
