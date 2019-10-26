from .database import *

def auth_logout(token):
    # when logout is called on a token it should be deleted from the currently active tokens dict.
    try:
        del update_data["tokens"][token]    # deleting the token from existance.
        return {'is_success' : True}        # now that the token has been deleted we return true
    except ValueError:
        print("session token is already invalid")   # value error if token dosent exist (i.e. invalid)