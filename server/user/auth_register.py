import re


def auth_register(email, password, name_first, name_last):
    check_regEmailtype(email)
    validate_regEmail(email)
    check_password_strength(password)
    check_first(name_first)
    check_last(name_last)
    uid = 1343254           #just for the testing 
    token = "something..."
    return {"u_id": uid, "token": token}

def check_regEmailtype(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        raise ValueError("this is not a valid email format!")

def validate_regEmail(email):
    #raise ValueError("error!!")
    # This will check if the email actually exists on the server
    # if it dosent then return true
    # filter out similar sub domains or high level domain
    # (z11@ad.unsw == z11@unsw)
    pass

def check_password_strength(password):
    # to check if the password is at least 5 digits
    if len(password) >= 5:
        return True
    else:
        raise ValueError("Password is too short!")

def check_first(name_first):
    # not more than 50 characters 
    if len(name_first) < 50:
        return True
    else:
        raise ValueError("first name is too long!")

def check_last(name_last):
    # not more than 50 characters
    if len(name_last) < 50:
        return True
    else:
        raise ValueError("first name is too long!")
