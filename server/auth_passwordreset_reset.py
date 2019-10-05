def auth_passwordreset_reset(reset_code, new_password):
    check_reset_code(reset_code)
    chec_password_strength(new_password)
    pass 

def check_reset_code(reset_code):
    # this will check if the reset code sent by the auth_passwordreset_request function is correct
    pass

def chec_password_strength(password):
    # to check if the password is at least 5 digits
    if len(password) >= 5:
        return True
    else:
        raise ValueError("Password is too short!")