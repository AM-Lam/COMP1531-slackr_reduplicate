from .database import *

def auth_logout(token):
    # when logout is called on a token it should be deleted from the currently active tokens dict.
    update_data = get_data()
    if token in update_data["tokens"]:      # if the token is in the currently active tokens list..
        del update_data["tokens"][token]    # deleting the token from existance.
        return {'is_success' : True}        # now that the token has been deleted we return true
    else:
        raise ValueError("session token is already invalid")