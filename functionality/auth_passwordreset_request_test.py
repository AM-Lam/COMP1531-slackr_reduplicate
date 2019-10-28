import pytest
from .database import clear_data, get_data
from .auth import auth_register, auth_passwordreset_request
from .access_error import *


def test_request_test():
    clear_data()
    
    auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')

    ## cant test this since send email code has been moved to server.py i.e. flask
    update_data = get_data()
    reset_code = auth_passwordreset_request('user1@domain.com')
    assert(update_data["reset"][reset_code]) == 'user1@domain.com'
    
